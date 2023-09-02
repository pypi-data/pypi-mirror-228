#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from ast import literal_eval
from urllib.parse import urlparse, parse_qsl

from flet_core import Page, RouteChangeEvent
from flet_core.types import AppView
from flet_runtime import app as flet_app

from flet_manager.views import ErrorView, BaseView


class App:
    title: str
    page: Page
    routes: dict
    theme: None
    session: None

    def __init__(
        self,
        title: str,
        main_view: type,
        error_view: type = ErrorView,
        views: list[BaseView] = None,
        theme: None = None,
        session: None = None,
        app_view: AppView = AppView.FLET_APP_WEB,
        **kwargs
    ):
        if not views:
            views = []

        self.title = title
        self.main_view_class = main_view
        self.main_view = None
        self.error_view = error_view
        self.theme = theme
        self.session = session
        self.routes = {}

        for view in views:
            self.routes[view.route] = view

        flet_app(target=self.start, view=app_view, **kwargs)

    async def view_pop(self, view):
        await self.view_change(go_back=True)

    async def view_change(self, view: BaseView = None, go_back: bool = False):
        if not self.page.views:
            view = self.main_view

        if go_back:
            self.page.views.pop()
        elif view:
            view.app = self
            await view.build()
            self.page.views.append(await view.get())

        await self.page.go_async(self.page.views[-1].route)
        await self.page.update_async()

    async def route_change(self, e: RouteChangeEvent):
        url = urlparse(e.route)
        route = url.path
        params = {}

        # Set params for view
        for key, value in dict(parse_qsl(url.query)).items():
            try:
                value = literal_eval(str(value))
            except ValueError:
                pass
            params[key] = value
        if self.page.views[-1].route == e.route:
            return

        # Go back if current == -2 view
        try:
            if self.page.views[-2].route == e.route:
                return await self.view_change(go_back=True)
        except IndexError:
            pass

        try:
            view = self.routes[route]
        except KeyError:
            view = self.error_view
            params['error_code'] = 404
        await self.view_change(view=view(**params))

    async def start(self, page: Page):
        self.page = page
        self.page.on_view_pop = self.view_pop
        self.page.on_route_change = self.route_change

        self.page.title = self.title

        self.main_view = self.main_view_class(app=self)
        self.page.views.clear()
        await self.view_change()
