# -*- coding: utf-8 -*-
# Code for Life
#
# Copyright (C) 2015, Ocado Limited
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ADDITIONAL TERMS – Section 7 GNU General Public Licence
#
# This licence does not grant any right, title or interest in any “Ocado” logos,
# trade names or the trademark “Ocado” or any other trademarks or domain names
# owned by Ocado Innovation Limited or the Ocado group of companies or any other
# distinctive brand features of “Ocado” as may be secured from time to time. You
# must not distribute any modification of this program using the trademark
# “Ocado” or claim any affiliation or association with Ocado or its employees.
#
# You are not authorised to use the name Ocado (or any of its trade names) or
# the names of any author or contributor in advertising or for publicity purposes
# pertaining to the distribution of this program, without the prior written
# authorisation of Ocado.
#
# Any propagation, distribution or conveyance of this program must include this
# copyright notice and these terms. You must not misrepresent the origins of this
# program; modified versions of the program must be marked as such and not
# identified as the original program.

from hamcrest import assert_that, equal_to
from portal.tests.pageObjects.portal.base_page import BasePage

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class GamePage(BasePage):
    def __init__(self, browser):
        super(GamePage, self).__init__(browser)

        assert self.on_correct_page('game_page')

        self._dismiss_initial_dialog()

    def _dismiss_initial_dialog(self):
        self.wait_for_element_by_id_to_be_clickable("play_button")
        self.browser.find_element_by_id("play_button").click()
        self.wait_for_element_by_id_to_be_invisible("play_button")
        return self

    def load_solution(self, workspace_id):
        self.browser.find_element_by_id("load_tab").click()
        selector = "#loadWorkspaceTable tr[value=\'" + str(workspace_id) + "\']"
        self.wait_for_element_to_be_clickable((By.CSS_SELECTOR, selector))
        self.browser.find_element_by_css_selector(selector).click()
        self.browser.find_element_by_id("loadWorkspace").click()
        return self

    def run_program(self):
        self.browser.find_element_by_id("play_tab").click()
        self.wait_for_element_to_be_clickable((By.ID, "routeScore"), 30)

        return self

    def _assert_score(self, element_id, score):
        route_score = self.browser.find_element_by_id(element_id).text
        assert_that(route_score, equal_to(score))
        return self

    def assert_route_score(self, score):
        return self._assert_score("routeScore", score)

    def assert_algorithm_score(self, score):
        return self._assert_score("algorithmScore", score)

    def wait_for_element_by_id(self, name, time=2):
        WebDriverWait(self.browser, time).until(
            EC.presence_of_element_located((By.ID, name))
        )

    def wait_for_element_by_id_to_be_clickable(self, name, time=5):
        self.wait_for_element_to_be_clickable((By.ID, name), time)

    def wait_for_element_to_be_clickable(self, locator, time=3):
        WebDriverWait(self.browser, time).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_element_by_id_to_be_invisible(self, name):
        WebDriverWait(self.browser, 3).until(
            EC.invisibility_of_element_located((By.ID, name))
        )