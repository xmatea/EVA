import matplotlib as plt
import globals
import PlotWindow



def Show_Plot_Window(self):
    print('in Show_plot_window')
    print(self.wp)

    if self.wp is None:
        self.wp = PlotWindow()
        self.wp.show()
        print('plotting')
        plt.fill_between(globals.x_GE1, globals.y_GE1, step='mid', color='yellow')
        plt.step(globals.x_GE1, globals.y_GE1, where='mid', color='black')
        plt.ylim(bottom=0.0)
        plt.xlabel("Energy")
        plt.ylabel("Intensity")
        plt.legend("yeah!")
        plt.title('Customized histogram')

        print('hello')

        # annot = plt.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
        #                    bbox=dict(boxstyle="round", fc="w"),
        #                    arrowprops=dict(arrowstyle="->"))
        # annot.set_visible(False)
        print('oops')

        def on_move(event):
            # get the x and y pixel coords
            x, y = event.x, event.y
            if event.inaxes:
                ax = event.inaxes  # the axes instance
                print('data coords %f %f' % (event.xdata, event.ydata))
                # annot.set_text(event.x,event.y)

        def on_click(event):
            if event.button is MouseButton.RIGHT:
                print('disconnecting callback')
                plt.disconnect(binding_id)

            if event.button is MouseButton.LEFT:
                x, y = event.x, event.y
                if event.inaxes:
                    ax = event.inaxes  # the axes instance
                    print('data coords this time are %f %f' % (event.xdata, event.ydata))

                    # need to store these
                    # annot.set_visible(True)
                    # annot.set_text(event.x)
                    plt.annotate(str(event.x) + " " + str(event.y), xy=(500, 500), xytext=(event.x, event.y))

        binding_id = plt.connect('motion_notify_event', on_move)
        plt.connect('button_press_event', on_click)

        plt.show()
