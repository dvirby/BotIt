from unittest import TestCase
from unittest.mock import MagicMock
import datetime

from BotFramework.bot_user import BotUser
from BotFramework.ui.button import Button

from BotFramework import TimeChooseView, Session, UI, ButtonMatrixView
from BotFramework.TestKit import TestKitUI
from BotFramework.ui.ignored_button import IgnoredButton


class TestTimeChooseAcitivty(TestCase):

    def _get_ui(self) -> UI:
        return TestKitUI()

    def _get_user(self) -> BotUser:
        user = MagicMock()

        return user

    def _get_button_matrix(self, time_choose: TimeChooseView, edit_mode: bool = False, able_to_save: bool = False) -> [[Button]]:
        matrix: [[Button]] = []

        if edit_mode:
            matrix += [[
                Button(TimeChooseView.EDIT, time_choose._edit)
            ]]

            return matrix

        #  Create button pad
        matrix += [[
            Button("1", time_choose._add_digit, 1),
            Button("2", time_choose._add_digit, 2),
            Button("3", time_choose._add_digit, 3),
        ]]

        matrix += [[
            Button("4", time_choose._add_digit, 4),
            Button("5", time_choose._add_digit, 5),
            Button("6", time_choose._add_digit, 6),
        ]]

        matrix += [[
            Button("7", time_choose._add_digit, 7),
            Button("8", time_choose._add_digit, 8),
            Button("9", time_choose._add_digit, 9),
        ]]

        matrix += [[
            Button("DEL", time_choose._remove_digit),
            Button("0", time_choose._add_digit, 0),
            IgnoredButton(TimeChooseView.EMPTY_BUTTON_TEXT),
        ]]

        if able_to_save:
            matrix += [[
                Button(TimeChooseView.SAVE, time_choose._save)
            ]]

        return matrix

    def _create_session(self, ui: UI) -> Session:
        return ui.create_session("TimeChoose", self._get_user())

    def test_create(self):
        ui = self._get_ui()
        session = self._create_session(ui)
        dt = datetime.datetime.now() + datetime.timedelta(days=3)
        dt = dt.replace(hour=13, minute=6)
        callback = lambda tv, ses, dt: None

        time_choose: TimeChooseView = TimeChooseView(
            session.view_container,
            choose_callback=callback,
            chosen_time=dt
        )

        #  Check parameters got currectly
        self.assertEqual(session.view_container, time_choose.view_container)
        self.assertEqual(time_choose.sub_container.ui, session.view_container.ui)
        self.assertEqual(time_choose.sub_container.session, session)
        self.assertEqual(callback, time_choose.choose_callback)
        self.assertEqual(dt, time_choose.chosen_time)

        # Not drawing anything in __init__
        self.assertEqual(0, len(time_choose.sub_container.views))

    def test_draw_with_time(self):
        ui = self._get_ui()
        session = self._create_session(ui)
        dt = datetime.datetime.now() + datetime.timedelta(days=3)
        dt = dt.replace(hour=13, minute=6)
        callback = lambda tv, ses, dt: None

        time_choose: TimeChooseView = TimeChooseView(
            session.view_container,
            choose_callback=callback,
            chosen_time=dt
        )

        time_choose.draw()

        self.assertEqual(time_choose.sub_container.views, [
            ButtonMatrixView(time_choose.sub_container,
                             TimeChooseView.TIME_CHOSEN + ":\n" \
                             + TimeChooseView.TIME_TEMPLATE % (1,3, 0,6),
                             self._get_button_matrix(time_choose, True)
                             )
        ])


    def test_draw_without_time(self):
        ui = self._get_ui()
        session = self._create_session(ui)
        callback = lambda tv, ses, dt: None

        time_choose: TimeChooseView = TimeChooseView(
            session.view_container,
            choose_callback=callback,
            chosen_time=None
        )

        time_choose.draw()

        self.assertEqual(time_choose.sub_container.views, [
            ButtonMatrixView(time_choose.sub_container,
                             TimeChooseView.TIME_CHOOSE + ":\n" \
                             + TimeChooseView.TIME_TEMPLATE % ('X','X', 'X','X'),
                             self._get_button_matrix(time_choose, False)
                             )
        ])

    def test_typing(self):
        ui = self._get_ui()
        session = self._create_session(ui)
        callback = lambda tv, ses, dt: None

        time_choose: TimeChooseView = TimeChooseView(
            session.view_container,
            choose_callback=callback,
            chosen_time=None
        )

        time_choose.draw()

        #  Add three digits (Not save mode yet)
        time_choose._add_digit(session, 1)
        time_choose._add_digit(session, 2)
        time_choose._add_digit(session, 9)

        self.assertEqual(time_choose.sub_container.views, [
            ButtonMatrixView(time_choose.sub_container,
                             TimeChooseView.TIME_CHOOSE + ":\n" \
                             + TimeChooseView.TIME_TEMPLATE % (1, 2, 9, 'X'),
                             self._get_button_matrix(time_choose, False, False),
                             )
        ])

        time_choose._add_digit(session, 3)

        self.assertEqual(time_choose.sub_container.views, [
            ButtonMatrixView(time_choose.sub_container,
                             TimeChooseView.TIME_CHOOSE + ":\n" \
                             + TimeChooseView.TIME_TEMPLATE % (1, 2, 9, 3),
                             self._get_button_matrix(time_choose, False, True),
                             )
        ])

        # Assert error is shown when save is pressed
        time_choose._save(session)

        self.assertEqual(time_choose.sub_container.views, [
            ButtonMatrixView(time_choose.sub_container,
                             TimeChooseView.TIME_CHOOSE + ":\n" \
                             + TimeChooseView.TIME_TEMPLATE % (1, 2, 9, 3) \
                             + "\n" + TimeChooseView.NOT_RIGHT_TIME_ERROR,
                             self._get_button_matrix(time_choose, False, True),
                             )
        ])

        time_choose._remove_digit(session)
        time_choose._remove_digit(session)

        # Assert error is disappered
        self.assertEqual(time_choose.sub_container.views, [
            ButtonMatrixView(time_choose.sub_container,
                             TimeChooseView.TIME_CHOOSE + ":\n" \
                             + TimeChooseView.TIME_TEMPLATE % (1, 2, 'X','X'),
                             self._get_button_matrix(time_choose, False, False),
                             )
        ])

        time_choose._add_digit(session, 4)
        time_choose._add_digit(session, 3)
        time_choose._save(session)

        self.assertEqual(time_choose.sub_container.views, [
            ButtonMatrixView(time_choose.sub_container,
                             TimeChooseView.TIME_CHOSEN + ":\n" \
                             + TimeChooseView.TIME_TEMPLATE % (1,2, 4,3),
                             self._get_button_matrix(time_choose, True),
                             )
        ])


