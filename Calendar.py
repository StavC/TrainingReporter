import calendar
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import inspect
import matplotlib.backends.backend_pdf

calendar.setfirstweekday(6) # Sunday is 1st day in US
w_days = 'ןושאר ינש ישילש יעיבר ישימח ישיש תבש'.split()
m_names = '''
ראוני ראורבפ ץרמ לירפא
יאמ ינוי ילוי טסוגוא
רבמטפס רבוטקוא רמבונ רבמצד'''.split()



class MplCalendar(object):
    def __init__(self, year, month):
        self.year = year
        self.month = month
        self.img=mpimg.imread("Inputs\\V.png")
        self.cal = calendar.monthcalendar(year, month)
        # monthcalendar creates a list of lists for each week
        # Save the events data in the same format
        self.events = [[[] for day in week] for week in self.cal]

    def _monthday_to_index(self, day):
        'The index of the day in the list of lists'
        day=int(day)
        for week_n, week in enumerate(self.cal):
            try:
                i = week.index(day)
                return week_n, i
            except ValueError:
                pass
         # couldn't find the day
        raise ValueError("There aren't {} days in the month".format(day))

    def add_event(self, day, event_str):
        'insert a string into the events list for the specified day'
        week, w_day = self._monthday_to_index(day)
        self.events[week][w_day].append(event_str)


    def show(self):
        'create the calendar'
        f, axs = plt.subplots(len(self.cal), 7, sharex=True, sharey=True,figsize=(8,7))
        for week, ax_row in enumerate(axs):
            for week_day, ax in enumerate(ax_row):
                ax.set_xticks([])
                ax.set_yticks([])
                if self.cal[week][week_day] != 0:
                    ax.text(.02, .98,
                            str(self.cal[week][week_day]),
                            verticalalignment='top',
                            horizontalalignment='left')
                contents = "\n".join(self.events[week][week_day])

                ax.text(.03, .85, contents,
                        verticalalignment='top',
                        horizontalalignment='left',
                        fontsize=9)
                if contents == "'":
                    ax.imshow(self.img,aspect='auto',interpolation='nearest')

        # use the titles of the first row as the weekdays
        for n, day in enumerate(w_days):
            axs[0][n].set_title(day)

        # Place subplots in a close grid
        f.subplots_adjust(hspace=0)
        f.subplots_adjust(wspace=0)
        f.suptitle(m_names[self.month-1] + ' ' + str(self.year),
                   fontsize=20, fontweight='bold')

        f.savefig('OutPuts\\Calander.png')
        plt.close(f)

