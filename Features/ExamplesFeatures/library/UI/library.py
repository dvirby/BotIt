from BotFramework import *
from BotFramework.Feature.bot_feature import BotFeature
from BotFramework.View.view import View
from BotFramework.session import Session
from BotFramework.UIbase.create_basic_ui import UI
from APIs.ExternalAPIs import *
from APIs.OtherAPIs.DatabaseRelated.User.user import User
from Features.ExamplesFeatures.library.Logic.Book import Book


class library(BotFeature):
    SS_ID = "1MZ0G3tfPLEokwd59yQVQyFM9_8Ej4B2bUzO5euh7HdU"
    SHEET = "sheet1"
    PLACE_OF_DATA = "A3:D800"
    ROW_OF_START = 3

    # init the class and call to super init - The same for every feature
    def __init__(self, ui: UI):
        super().__init__(ui)

    def main(self, session: Session):
        """
        Called externally when the user starts the feature. The BotManager
        creates a dedicated Session for the user and the feature, and asks
        the feature using this function to send the initial Views to him.
        :param session: Session object
        :return: nothing
        """
        buttons = [self.ui.create_button_view("ספריית עיון", self.sifreyIun)]
                   # self.UIbase.create_button_view("ספריית לימוד", self.sifreyLimud)]

        buttons_list = self.ui.create_button_group_view(session, "איזו ספריה אתה מעוניין?", buttons)
        buttons_list.draw()

    def sifreyIun(self, session):
        self.ui.create_text_view(session, "הכנס שם של ספר").draw()
        self.ui.get_text(session, self.getFromBookName)

    def get_free_sheet_row(self, spreadsheet_id, sheet_name, last_column_index):
        """
        :param spreadsheet_id: The ID of the GoogleSheet document
        :param sheet_name: Inside the document, what sheet to use
        :param last_column_index: the last column index to check if empty
        :return the first row in the google sheets file which is free. Free means that all the cells in the row until
        the last_column index are empty
        """
        with GoogleSheets.get_instance() as gs:
            row = 1
            while True:
                test_list = gs.get_range(spreadsheet_id, sheet_name,
                                         "A" + str(row) + ":" + str(last_column_index) + str(row))
                if test_list is None:
                    break
                row += 1
        return row

    def getFromBookName(self, session, bookName: str):
        bookDict = {}

        with GoogleSheets.get_instance() as gs:
            data = gs.get_range(self.SS_ID, self.SHEET, self.PLACE_OF_DATA)
            row = 0
            for content in data:
                if len(content) < 4:
                    content.append("")
                try:
                    bookDict[content[0]] = Book(content[0], content[1], content[2], content[3],
                                                row + self.ROW_OF_START)
                except:
                    continue
                row += 1

        def try_again(session) -> None:
            """This function call after the user press the try again button
            :return: None
            """
            self.ui.clear(session)
            self.sifreyIun(session)

        self.ui.create_closest_name_view(session, bookDict, bookName, 5, self.getBook,
                                         try_again).draw()

    def getBook(self, session, activity: ClosestNameActivity, book: Book):
        self.ui.clear(session)
        msg = "הספר שבחרת הוא: " + book.nameBook + "\n" + "מאת: " + book.author + "\n" + "הכמות שיש במלאי היא: " + book.numOfCopies
        self.ui.create_text_view(session, msg).draw()
        buttons = []
        borrow_list = book.listOfBorrow
        cur_name = session.user.name
        if cur_name in borrow_list or " " + cur_name in borrow_list:
            buttons.append(self.ui.create_button_view("להחזיר", lambda s: self.returnBook(s, book)))
        else:
            if int(book.numOfCopies) > 0:
                buttons.append(
                    self.ui.create_button_view("לשאול", lambda s: self.borrowBook(s, book)))
            else:
                msg = "לצערנו לא נשארו עותקים של הספר" + "\n" + " זוהי רשימת השואלים: " + book.listOfBorrow
                self.ui.create_text_view(session,
                                         msg).draw()

        if len(buttons) == 0:
            self.ui.create_text_view(session,
                                     "לא ניתן לבצע פעולות על הספר").draw()
        else:
            buttons_list = self.ui.create_button_group_view(session, "מה אתה מעוניין לבצע?",
                                                            buttons)
            buttons_list.draw()

    def borrowBook(self, session, book: Book):
        with GoogleSheets.get_instance() as gc:
            book.numOfCopies = str(int(book.numOfCopies) - 1)
            gc.set_range(self.SS_ID, self.SHEET, 'B' + str(book.row),
                         [[book.numOfCopies]])
            # add the name to list of borrow
            if len(book.listOfBorrow) == 0:
                book.listOfBorrow += session.user.name
            else:
                book.listOfBorrow += ", " + session.user.name
            gc.set_range(self.SS_ID, self.SHEET, 'D' + str(book.row),
                         [[book.listOfBorrow]])

        self.ui.summarize_and_close(session,
                                    [self.ui.create_text_view(session, "זכור להחזיר! :)")
                                     ], True)

    def returnBook(self, session, book: Book):
        with GoogleSheets.get_instance() as gc:
            book.numOfCopies = str(int(book.numOfCopies) + 1)
            gc.set_range(self.SS_ID, self.SHEET, 'B' + str(book.row), [[book.numOfCopies]],
                         )
            # remove the cur user from the list of borrow
            borrow_list = book.listOfBorrow.split(",")
            cur_name = session.user.name
            if cur_name in borrow_list:
                borrow_list.remove(cur_name)
            elif " " + cur_name in borrow_list:
                borrow_list.remove(" " + cur_name)
            book.listOfBorrow = ','.join(borrow_list)
            gc.set_range(self.SS_ID, self.SHEET, 'D' + str(book.row), [[book.listOfBorrow]],
                         )

        self.ui.summarize_and_close(session,
                                    [self.ui.create_text_view(session, "תודה שזכרת להחזיר! :)")
                                     ], True)

    def sifreyLimud(self, seasson):
        pass

    def send_text_back_to_usr(self, session, usr_string):
        self.ui.create_text_view(session, usr_string).draw()

    def get_summarize_views(self, session: Session) -> [View]:
        """
        Called externally when the BotManager wants to close this feature.
        This function returns an array of views that summarize the current
        status of the session. The array can be empty.
        :param session: Session object
        :return: Array of views summarizing the current feature Status.
        """
        pass

    def is_authorized(self, user: User) -> bool:
        """
        A function to test if a user is authorized to use this feature.
        :param user: the user to test
        :return: True if access should be allowed, false if should be restricted.
        """
        return "reg_user" in user.role

    def get_scheduled_jobs(self) -> [ScheduledJob]:
        """
        Get jobs (scheduled functions) that need to be called at specific times.
        :return: List of Jobs that will be created and called.
        """
        return []
