from tkinter import *
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Dashboard2:
    def __init__(self, frame):
        self.frame = frame
        self.frame.config(bg="white")

        self.theme = 'light'  # Default theme
        self.colors = self.get_colors(self.theme)

        # body frame 1
        self.bodyFrame1 = Frame(self.frame, bg=self.colors['body_frame'])
        self.bodyFrame1.place(x=20, y=20, width=1300, height=350)

        # body frame 2
        self.bodyFrame2 = Frame(self.frame, bg=self.colors['body_frame2'])
        self.bodyFrame2.place(x=20, y=380, width=310, height=220)

        # body frame 3
        self.bodyFrame3 = Frame(self.frame, bg=self.colors['body_frame3'])
        self.bodyFrame3.place(x=340, y=380, width=310, height=220)

        # body frame 4
        self.bodyFrame4 = Frame(self.frame, bg=self.colors['body_frame4'])
        self.bodyFrame4.place(x=660, y=380, width=310, height=220)

        # Body Frame 1 with Graphs
        self.show_graphs(self.bodyFrame1)

        # Body Frame 2
        self.total_people = Label(self.bodyFrame2, text='230', bg=self.colors['body_frame2'], font=("", 25, "bold"))
        self.total_people.place(x=120, y=100)

        self.totalPeopleImage = ImageTk.PhotoImage(file='images/left-icon.png')
        self.totalPeople = Label(self.bodyFrame2, image=self.totalPeopleImage, bg=self.colors['body_frame2'])
        self.totalPeople.place(x=220, y=0)

        self.totalPeople_label = Label(self.bodyFrame2, text="Total People", bg=self.colors['body_frame2'],
                                       font=("", 12, "bold"),
                                       fg=self.colors['fg'])
        self.totalPeople_label.place(x=5, y=5)

        # Body Frame 3
        self.people_left = Label(self.bodyFrame3, text='50', bg=self.colors['body_frame3'], font=("", 25, "bold"))
        self.people_left.place(x=120, y=100)

        # left icon
        self.LeftImage = ImageTk.PhotoImage(file='images/left-icon.png')
        self.Left = Label(self.bodyFrame3, image=self.LeftImage, bg=self.colors['body_frame3'])
        self.Left.place(x=220, y=0)

        self.peopleLeft_label = Label(self.bodyFrame3, text="Left", bg=self.colors['body_frame3'],
                                      font=("", 12, "bold"),
                                      fg=self.colors['fg'])
        self.peopleLeft_label.place(x=5, y=5)

        # Body Frame 4
        self.total_earnings = Label(self.bodyFrame4, text='$40,000.00', bg=self.colors['body_frame4'],
                                    font=("", 25, "bold"))
        self.total_earnings.place(x=80, y=100)

        self.earnings_label = Label(self.bodyFrame4, text="Total Earnings", bg=self.colors['body_frame4'],
                                    font=("", 12, "bold"),
                                    fg=self.colors['fg'])
        self.earnings_label.place(x=5, y=5)

        # Frame 4 icon
        self.earningsIcon_image = ImageTk.PhotoImage(file='images/earn3.png')
        self.earningsIcon = Label(self.bodyFrame4, image=self.earningsIcon_image, bg=self.colors['body_frame4'])
        self.earningsIcon.place(x=220, y=0)

    def get_colors(self, theme):
        if theme == 'dark':
            return {
                'bg': '#2e2e2e',
                'body_frame': '#3e3e3e',
                'body_frame2': '#4e4e4e',
                'body_frame3': '#5e5e5e',
                'body_frame4': '#6e6e6e',
                'heading': '#ffffff',
                'fg': '#ffffff'
            }
        else:
            return {
                'bg': '#eff5f6',
                'body_frame': '#ffffff',
                'body_frame2': '#009aa5',
                'body_frame3': '#e21f26',
                'body_frame4': '#ffcb1f',
                'heading': '#0064d3',
                'fg': '#000000'
            }

    def show_graphs(self, frame):
        # Pie chart data
        labels = ['Python', 'C++', 'Ruby', 'Java']
        sizes = [215, 130, 245, 210]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
        explode = (0.1, 0, 0, 0)  # explode 1st slice

        fig1, ax1 = plt.subplots(figsize=(6, 3))  # Ajusta el tamaño para que sea más ancho
        ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
                shadow=True, startangle=140)
        ax1.axis('equal')

        pie_chart = FigureCanvasTkAgg(fig1, master=frame)
        pie_chart.draw()
        pie_chart.get_tk_widget().pack(side=LEFT, padx=(10, 5), pady=10, fill=BOTH, expand=True)

        # Bar chart data
        objects = ('Python', 'C++', 'Ruby', 'Java', 'Perl')
        y_pos = np.arange(len(objects))
        performance = [10, 8, 6, 4, 2]

        fig2, ax2 = plt.subplots(figsize=(6, 3))  # Ajusta el tamaño para que sea más ancho
        ax2.bar(y_pos, performance, align='center', alpha=0.5)
        ax2.set_xticks(y_pos)
        ax2.set_xticklabels(objects)
        ax2.set_ylabel('Usage')
        ax2.set_title('Programming language usage')

        bar_chart = FigureCanvasTkAgg(fig2, master=frame)
        bar_chart.draw()
        bar_chart.get_tk_widget().pack(side=LEFT, padx=(5, 10), pady=10, fill=BOTH, expand=True)

def main(frame):
    # Inicializar Dashboard2 dentro del frame
    Dashboard2(frame)
