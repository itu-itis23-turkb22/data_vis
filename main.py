import tkinter as tk
from tkinter import font as tkfont
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sqlite3
import bcrypt
import pathlib


class Window(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._frame = None
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Data Visualizer")
        self["padx"] = 75
        self["pady"] = 25
        self.show_frame(LoginPage)

    def show_frame(self, frame_class):
        self.geometry("550x200")
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid(row=0, column=0)


class LoginPage(tk.Frame):


    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        parent.geometry("500x200")

        def login_func():
            global logged_username
            username_data = hash_the_data(username_input.get().encode())
            password_data = hash_the_data(password_input.get().encode())
            db_connection = sqlite3.connect("user_data.db")
            db_cursor = db_connection.cursor()
            db_cursor.execute("SELECT password FROM login_Data WHERE username =?", (username_data,))
            results_ = db_cursor.fetchall()
            if len(results_) == 0:
                warning_.configure(text="!WRONG USERNAME OR NOT REGISTERED!")
            elif results_[0][0] == password_data:
                warning_.configure(text="Successfully logged in")
                logged_username = username_input.get()
                parent.show_frame(MainMenu)
            else:
                warning_.configure(text="!WRONG PASSWORD!")
            db_connection.close()


        def hash_the_data(inpt_):
            salt = b'$2b$12$2mjqFWiHOdMqeKpSZEyrQO'
            if type(inpt_) != bytes:
                inpt_ = inpt_.encode()
            hashed_inpt_ = bcrypt.hashpw(inpt_, salt)
            return hashed_inpt_

        def register_func():
            username_data = hash_the_data(username_input.get().encode())
            password_data = hash_the_data(password_input.get().encode())
            create_table_if_not_exists()
            db_connection = sqlite3.connect("user_data.db")
            db_cursor = db_connection.cursor()
            db_cursor.execute("SELECT username FROM login_Data WHERE username=?", (username_data,))
            results_ = db_cursor.fetchall()
            if len(results_) == 0:
                if len(password_input.get()) < 7:
                    warning_.configure(text="PASSWORD IS TOO SHORT")
                else:
                    db_cursor.execute("INSERT INTO login_data VALUES(?,?)", (username_data, password_data))
                    db_connection.commit()
                    username_input.delete(0, len(username_input.get()))
                    password_input.delete(0, len(password_input.get()))
            else:
                warning_.configure(text="!You Are Already Registered!")
            db_connection.close()

        def create_table_if_not_exists():
            db_connection = sqlite3.connect("user_data.db")
            db_cursor = db_connection.cursor()
            db_cursor.execute("CREATE TABLE IF NOT EXISTS login_data(username TEXT, password TEXT)")
            db_connection.commit()
            db_connection.close()

        create_table_if_not_exists()
        info_label = tk.Label(self, text="LOGIN")
        info_label.grid(row=0, column=1)

        info_username = tk.Label(self, text="Username:")
        info_username.grid(row=1, column=0)
        username_input = tk.Entry(self)
        username_input.grid(row=1, column=1)

        info_password = tk.Label(self, text="Password:")
        info_password.grid(row=2, column=0)
        password_input = tk.Entry(self, show="*")
        password_input.grid(row=2, column=1)

        info_register = tk.Label(self, text="!!  If you dont have an account please use register button"
                                                   "\nIf you already have an account use the login button")
        info_register.grid(row=3, column=0, columnspan=4)
        register_button = tk.Button(self, text="Register", command=register_func)
        register_button.grid(row=4, column=0)
        login_button = tk.Button(self, text="Login", command=login_func)
        login_button.grid(row=4, column=1)

        warning_ = tk.Label(self, text="")
        warning_.grid(row=5, column=1)


class MainMenu(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        parent.geometry("550x250")
        info_label = tk.Label(self, text="Welcome to the Berkay's Data Visualizer. Please choose what you want to do.\n"
                                         "Also if you want to work with xlsx file please be sure that you get rid of\n"
                                         "any unnecessary rows at the top of the file", pady=20)
        new_file_button = tk.Button(self, text="Add new file", command=lambda: parent.show_frame(NewFileMenu))
        old_file_button = tk.Button(self, text="Edit old file", command=lambda: parent.show_frame(OldFileMenu))
        new_function_button = tk.Button(self,text="Add Function", command= lambda: parent.show_frame(NewFunctionMenu))
        button = tk.Button(self, text="Log Out", command=lambda: parent.show_frame(LoginPage))
        empty_label = tk.Label(self, text="\n\n\n\n")
        info_label.grid(row=0, column=0, columnspan=4)
        new_file_button.grid(row=1, column=0)
        new_function_button.grid(row=1, column=2)
        old_file_button.grid(row=1, column=3)
        empty_label.grid(row=2)
        button.grid(row=3, column=5)


class NewFunctionMenu(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        def create_table_if_not_exists():
            db_connection = sqlite3.connect("user_data.db")
            db_cursor = db_connection.cursor()
            db_cursor.execute("""CREATE TABLE IF NOT EXISTS file_data(
            username TEXT,
            filename TEXT,
            filetype TEXT,
            filepath TEXT,
            dimension TEXT,
            graphtype TEXT,
            xname TEXT,
            yname TEXT,
            zname TEXT 
             )""")
            db_connection.commit()
            db_connection.close()

        create_table_if_not_exists()

        def button_command():
            db_connection = sqlite3.connect("user_data.db")
            db_cursor = db_connection.cursor()
            db_cursor.execute("SELECT filename FROM file_data WHERE (filename=? AND username=?) ",
                                  (new_file_name_input.get(), logged_username))
            results = db_cursor.fetchall()
            if len(results) == 0:
                db_cursor.execute("INSERT INTO file_data VALUES(?,?,?,?,?,?,?,?,?)", (logged_username,
                                                                                      new_file_name_input.get(),
                                                                                      "function",
                                                                                      "",
                                                                                      "",
                                                                                      "",
                                                                                      name_x_input.get(),
                                                                                      name_y_input.get(),
                                                                                      ""
                                                                                      ))
                db_connection.commit()
                parent.show_frame(MainMenu)
            elif len(results) == 1:
                warning_.configure(text="Name of the function already exists")

        parent.geometry("500x300")
        new_file_name_label = tk.Label(self, text="Please give a name to the function:")
        name_x = tk.Label(self, text="Range of X values:"
                                     "\n(input like shown or errors will occur:"
                                     "\n(min,max,number of x values))")
        name_y = tk.Label(self, text="Function(y=?):"
                                     "\n(Please enter a math function of x\n "
                                     "that can be executed in Python)")
        warning_ = tk.Label(self, text="")

        name_x_input = tk.Entry(self)
        name_y_input = tk.Entry(self)
        new_file_name_input = tk.Entry(self)

        new_file_button = tk.Button(self, text="Add new function", command=lambda: button_command())
        go_back_button = tk.Button(self, text="Go Back", command=lambda: parent.show_frame(MainMenu))

        new_file_name_input.grid(row=0, column=1)
        new_file_name_label.grid(row=0, column=0)
        name_x.grid(row=2, column=0)
        name_y.grid(row=3, column=0)
        name_x_input.grid(row=2, column=1)
        name_y_input.grid(row=3, column=1)
        new_file_button.grid(row=4, column=0, columnspan=2, pady=10)
        warning_.grid(row=5, column=0, columnspan=2)
        go_back_button.grid(row=6, column=0, columnspan=2)


class NewFileMenu(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        def create_table_if_not_exists():
            db_connection = sqlite3.connect("user_data.db")
            db_cursor = db_connection.cursor()
            db_cursor.execute("""CREATE TABLE IF NOT EXISTS file_data(
            username TEXT,
            filename TEXT,
            filetype TEXT,
            filepath TEXT,
            dimension TEXT,
            graphtype TEXT,
            xname TEXT,
            yname TEXT,
            zname TEXT 
             )""")
            db_connection.commit()
            db_connection.close()
        create_table_if_not_exists()

        def button_command():
            try:
                path_checker = open(path_input.get())
                path_checker.close()
                db_connection = sqlite3.connect("user_data.db")
                db_cursor = db_connection.cursor()
                db_cursor.execute("SELECT filename FROM file_data WHERE (filename=? AND username=?) ", (new_file_name_input.get(),logged_username))
                results = db_cursor.fetchall()
                if len(results) == 0:
                    db_cursor.execute("INSERT INTO file_data VALUES(?,?,?,?,?,?,?,?,?)", (logged_username,
                                                                                          new_file_name_input.get(),
                                                                                          pathlib.Path(path_input.get()).suffix,
                                                                                          path_input.get(),
                                                                                          dataset_dimension_input.get(),
                                                                                          graph_type_input.get(),
                                                                                          name_x_input.get(),
                                                                                          name_y_input.get(),
                                                                                          name_z_input.get()
                                                                                          ))
                    db_connection.commit()
                elif len(results) == 1:
                    raise TypeError
                warning_.configure(text="")
                parent.show_frame(MainMenu)
            except :
                warning_.configure(text="Something went wrong. Check the filepath,be sure that file \n"
                                        "name is unique,check if the graph type is suitable for dataset dimensions\n"
                                        "check if the file contains integer values and x y z names are correct ")

        parent.geometry("500x300")
        new_file_name_label = tk.Label(self,text="Please give a name to the file:")
        new_file_info_label = tk.Label(self, text="Please enter the path of the file:")
        dataset_dimension_info_label = tk.Label(self,text="Is it a 2D or 3D dataset?(2D or 3D):")
        graph_type_info_label = tk.Label(self, text="What type of graph do you want:"
                                                    "\n(For 2d datasets: line, bar)"
                                                    "\n(For 3d datasets: line, point)")
        name_x = tk.Label(self, text="Name of x values")
        name_y = tk.Label(self, text="Name of y values")
        name_z = tk.Label(self, text="Name of z values\n(For 3D datasets)")
        warning_ = tk.Label(self, text="")

        name_x_input = tk.Entry(self)
        name_y_input = tk.Entry(self)
        name_z_input = tk.Entry(self)
        graph_type_input = tk.Entry(self)
        dataset_dimension_input = tk.Entry(self)
        path_input = tk.Entry(self)
        new_file_name_input = tk.Entry(self)

        new_file_button = tk.Button(self, text="Add new file", command=lambda: button_command())
        go_back_button = tk.Button(self, text="Go Back", command=lambda: parent.show_frame(MainMenu))

        new_file_name_input.grid(row=0, column=2, columnspan=2)
        new_file_name_label.grid(row=0, column=0, columnspan=2)
        new_file_info_label.grid(row=1, column=0, columnspan=2)
        path_input.grid(row=1, column=2, columnspan=2)
        dataset_dimension_info_label.grid(row=2, column=0, columnspan=2)
        dataset_dimension_input.grid(row=2, column=2, columnspan=2)
        graph_type_info_label.grid(row=3, rowspan=3, column=0, columnspan=2)
        graph_type_input.grid(row=3, column=2, columnspan=2)
        name_x.grid(row=6, column=0)
        name_y.grid(row=6, column=1)
        name_z.grid(row=6, column=2)
        name_x_input.grid(row=7, column=0)
        name_y_input.grid(row=7, column=1)
        name_z_input.grid(row=7, column=2)
        new_file_button.grid(row=8, column=0, columnspan=4, pady=10)
        warning_.grid(row=9, column=0, columnspan=5)
        go_back_button.grid(row=10, column=0, columnspan=4)


class OldFileMenu(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        parent.geometry("300x400")

        def create_table_if_not_exists():
            db_connection = sqlite3.connect("user_data.db")
            db_cursor = db_connection.cursor()
            db_cursor.execute("""CREATE TABLE IF NOT EXISTS file_data(
            username TEXT,
            filename TEXT,
            filetype TEXT,
            filepath TEXT,
            dimension TEXT,
            graphtype TEXT,
            xname TEXT,
            yname TEXT,
            zname TEXT 
             )""")
            db_connection.commit()
            db_connection.close()
        create_table_if_not_exists()
        db_connection = sqlite3.connect("user_data.db")
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT filename FROM file_data WHERE username=?", (logged_username,))
        filenames = db_cursor.fetchall()

        def csv_graph_line(fname, path, xname, yname):
            data = pd.read_csv(path)
            data[yname] = data[yname].astype(int)
            try:
                data[xname] = data[xname].astype(str)
            except:
                pass
            plt.plot(data[xname], data[yname])
            plt.title(fname)
            plt.xlabel(xname.upper())
            plt.ylabel(yname.upper())

            plt.show()

        def csv_graph_bar(fname, path, xname, yname):
            data = pd.read_csv(path)
            data[yname] = data[yname].astype(int)
            try:
                data[xname] = data[xname].astype(str)
            except:
                pass
            plt.bar(data[xname], data[yname])
            plt.title(fname)
            plt.xlabel(xname.upper())
            plt.ylabel(yname.upper())

            plt.show()

        def three_d_line_csv(path, xname, yname, zname):
            data = pd.read_csv(path)
            ax = plt.axes(projection='3d')

            ax.plot3D(data[xname], data[yname], data[zname], 'gray')
            plt.show()

        def three_d_point_csv(path, xname, yname, zname):
            data = pd.read_csv(path)
            ax = plt.axes(projection='3d')

            ax.scatter3D(data[xname], data[yname], data[zname], cmap="Greens")
            plt.show()

        def xlsx_graph_line(fname, path, xname, yname):
            data = pd.read_excel(path)
            data[yname] = data[yname].astype(int)
            try:
                data[xname] = data[xname].astype(str)
            except:
                pass
            plt.plot(data[xname], data[yname])
            plt.title(fname)
            plt.xlabel(xname.upper())
            plt.ylabel(yname.upper())

            plt.show()

        def xlsx_graph_bar(fname, path, xname, yname):
            data = pd.read_excel(path)
            data[yname] = data[yname].astype(int)
            try:
                data[xname] = data[xname].astype(str)
            except:
                pass
            plt.bar(data[xname], data[yname])
            plt.title(fname)
            plt.xlabel(xname.upper())
            plt.ylabel(yname.upper())

            plt.show()

        def three_d_line_xlsx(path, xname, yname, zname):
            data = pd.read_excel(path)

            ax = plt.axes(projection='3d')
            data = data.sort_values(xname)

            ax.plot3D(data[xname], data[yname], data[zname], 'gray')
            plt.show()

        def three_d_point_xlsx(path, xname, yname, zname):
            data = pd.read_excel(path)

            ax = plt.axes(projection='3d')
            ax.scatter3D(data[xname], data[yname], data[zname], cmap="Greens")
            plt.show()

        def function_visualize(fname, xname, yname):
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.spines['left'].set_position('center')
            ax.spines['bottom'].set_position('center')
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')
            x = eval("np.linspace" + xname)
            y = eval(yname)
            plt.plot(x, y, 'r')
            plt.title(fname)
            plt.show()

        def delete_draft():
            db_cursor.execute("DELETE FROM file_data WHERE (filename=? and username=?)",
                              (old_file_listbox.get("anchor")[0], logged_username))
            db_connection.commit()
            old_file_listbox.delete("anchor")

        def edit_draft():
            global anchored_file_data
            anchored_filename = old_file_listbox.get("anchor")[0]
            db_cursor.execute("SELECT * FROM file_data WHERE (filename=? and username=?)",
                              (anchored_filename, logged_username))
            anchored_file_data = db_cursor.fetchall()[0]
            if anchored_file_data[2] != "function":
                parent.show_frame(EditFileMenu)
            else:
                parent.show_frame(EditFunctionMenu)

        def visualize_draft():
            anchored_filename = old_file_listbox.get("anchor")[0]
            db_cursor.execute("SELECT * FROM file_data WHERE (filename=? and username=?)",
                              (anchored_filename, logged_username))
            draft_data = db_cursor.fetchall()[0]
            if draft_data[2] == ".csv":
                if draft_data[4].lower() == "2d" and draft_data[7] != "" and draft_data[6] != "":
                    if draft_data[5].lower() == "line":
                        filename = draft_data[1]
                        filepath = draft_data[3]
                        x_name = draft_data[6]
                        y_name = draft_data[7]
                        csv_graph_line(filename, filepath, x_name, y_name)

                    elif draft_data[5].lower() == "bar":
                        filename = draft_data[1]
                        filepath = draft_data[3]
                        x_name = draft_data[6]
                        y_name = draft_data[7]
                        csv_graph_bar(filename, filepath, x_name, y_name)

                    else:
                        old_file_label.configure(text="Unknown graph type"
                                                      "\nPlease edit the draft")

                elif draft_data[4].lower() == "3d" and draft_data[8] != "" and draft_data[7] != "" and draft_data[6] != "":
                    if draft_data[5].lower() == "line":
                        filepath = draft_data[3]
                        x_name = draft_data[6]
                        y_name = draft_data[7]
                        z_name = draft_data[8]
                        three_d_line_csv(filepath, x_name, y_name, z_name)

                    elif draft_data[5].lower() == "point":
                        filepath = draft_data[3]
                        x_name = draft_data[6]
                        y_name = draft_data[7]
                        z_name = draft_data[8]
                        three_d_point_csv(filepath, x_name, y_name, z_name)

                else:
                    old_file_label.configure(text="Please check the dimensions of"
                                                  "\nthe dataset, and be sure that"
                                                  "\nyou named every dimension in dataset")
            elif draft_data[2] == "function":
                filename = draft_data[1]
                x_name = draft_data[6]
                y_name = draft_data[7]
                function_visualize(filename, x_name, y_name)

            elif draft_data[2] == ".xlsx":
                if draft_data[4].lower() == "2d" and draft_data[7] != "" and draft_data[6] != "":
                    if draft_data[5].lower() == "line":
                        filename = draft_data[1]
                        filepath = draft_data[3]
                        x_name = draft_data[6]
                        y_name = draft_data[7]
                        xlsx_graph_line(filename, filepath, x_name, y_name)

                    elif draft_data[5].lower() == "bar":
                        filename = draft_data[1]
                        filepath = draft_data[3]
                        x_name = draft_data[6]
                        y_name = draft_data[7]
                        xlsx_graph_bar(filename, filepath, x_name, y_name)

                    else:
                        old_file_label.configure(text="Unknown graph type for 2D")
                elif draft_data[4].lower() == "3d" and draft_data[8] != "" and draft_data[7] != "" and draft_data[6] != "":
                    if draft_data[5].lower() == "line":
                        filepath = draft_data[3]
                        x_name = draft_data[6]
                        y_name = draft_data[7]
                        z_name = draft_data[8]
                        three_d_line_xlsx(filepath, x_name, y_name, z_name)

                    elif draft_data[5].lower() == "point":
                        filepath = draft_data[3]
                        x_name = draft_data[6]
                        y_name = draft_data[7]
                        z_name = draft_data[8]
                        three_d_point_xlsx(filepath, x_name, y_name, z_name)
            else:
                old_file_label.configure(text="Unknown file format")

        old_file_label = tk.Label(self, text="This is old file menu")
        old_file_listbox = tk.Listbox(self)
        go_back_button = tk.Button(self, text="Go Back to Main Page", command=lambda: parent.show_frame(MainMenu))
        delete_button = tk.Button(self, text="Delete the draft", command=delete_draft)
        edit_button = tk.Button(self, text="Edit the draft", command=edit_draft)
        visualize_button = tk.Button(self, text="Show Visualization", command=visualize_draft)

        for i in filenames:
            old_file_listbox.insert(0, i)

        go_back_button.grid(row=99, column=0, pady=5)
        delete_button.grid(row=2, column=0, pady=5, padx=10)
        edit_button.grid(row=3, column=0, pady=5, padx=10)
        visualize_button.grid(row=4, column=0, pady=5, padx=10)
        old_file_label.grid(row=0, column=0, pady=5)
        old_file_listbox.grid(row=1, column=0, pady=5)


class EditFileMenu(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        def create_table_if_not_exists():
            db_connection = sqlite3.connect("user_data.db")
            db_cursor = db_connection.cursor()
            db_cursor.execute("""CREATE TABLE IF NOT EXISTS file_data(
            username TEXT,
            filename TEXT,
            filetype TEXT,
            filepath TEXT,
            dimension TEXT,
            graphtype TEXT,
            xname TEXT,
            yname TEXT,
            zname TEXT 
             )""")
            db_connection.commit()
            db_connection.close()
        create_table_if_not_exists()

        def button_command():
            try:
                path_checker = open(path_input.get())
                path_checker.close()
                db_connection = sqlite3.connect("user_data.db")
                db_cursor = db_connection.cursor()
                db_cursor.execute("DELETE FROM file_data WHERE (filename=? AND username=?)",
                                  (anchored_file_data[1], logged_username))
                db_connection.commit()
                db_cursor.execute("SELECT filename FROM file_data WHERE (filename=? AND username=?)",
                                  (new_file_name_input.get(), logged_username))
                results = db_cursor.fetchall()
                if len(results) == 0:
                    db_cursor.execute("INSERT INTO file_data VALUES(?,?,?,?,?,?,?,?,?)", (logged_username,
                                                                                          new_file_name_input.get(),
                                                                                          pathlib.Path(path_input.get()).suffix,
                                                                                          path_input.get(),
                                                                                          dataset_dimension_input.get(),
                                                                                          graph_type_input.get(),
                                                                                          name_x_input.get(),
                                                                                          name_y_input.get(),
                                                                                          name_z_input.get()
                                                                                          ))
                    db_connection.commit()
                elif len(results) == 1:
                    raise TypeError
                warning_.configure(text="")
                parent.show_frame(OldFileMenu)
            except:
                warning_.configure(text="Something went wrong. Check the filepath,be sure that file \n"
                                        "name is unique,check if the graph type is suitable for dataset dimensions\n"
                                        "check if the file contains integer values and x y z names are correct ")

        parent.geometry("500x300")
        new_file_name_label = tk.Label(self,text="Please give a name to the file:")
        new_file_info_label = tk.Label(self, text="Please enter the path of the file:")
        dataset_dimension_info_label = tk.Label(self,text="Is it a 2D or 3D dataset?(2D or 3D):")
        graph_type_info_label = tk.Label(self, text="What type of graph do you want:"
                                                    "\n(For 2d datasets: line, bar)"
                                                    "\n(For 3d datasets: line, point)")
        name_x = tk.Label(self, text="Name of x values")
        name_y = tk.Label(self, text="Name of y values")
        name_z = tk.Label(self, text="Name of z values\n(For 3D datasets)")
        warning_ = tk.Label(self, text="")

        name_x_input = tk.Entry(self)
        name_x_input.insert(0, anchored_file_data[6])
        name_y_input = tk.Entry(self)
        name_y_input.insert(0, anchored_file_data[7])
        name_z_input = tk.Entry(self)
        name_z_input.insert(0, anchored_file_data[8])
        graph_type_input = tk.Entry(self)
        graph_type_input.insert(0, anchored_file_data[5])
        dataset_dimension_input = tk.Entry(self)
        dataset_dimension_input.insert(0, anchored_file_data[4])
        path_input = tk.Entry(self)
        path_input.insert(0, anchored_file_data[3])
        new_file_name_input = tk.Entry(self)
        new_file_name_input.insert(0, anchored_file_data[1])

        new_file_button = tk.Button(self, text="Edit File", command=button_command)
        go_back_button = tk.Button(self, text="Go Back", command=lambda: parent.show_frame(OldFileMenu))

        new_file_name_input.grid(row=0, column=2, columnspan=2)
        new_file_name_label.grid(row=0, column=0, columnspan=2)
        new_file_info_label.grid(row=1, column=0, columnspan=2)
        path_input.grid(row=1, column=2, columnspan=2)
        dataset_dimension_info_label.grid(row=2, column=0, columnspan=2)
        dataset_dimension_input.grid(row=2, column=2, columnspan=2)
        graph_type_info_label.grid(row=3, rowspan=3, column=0, columnspan=2)
        graph_type_input.grid(row=3, column=2, columnspan=2)
        name_x.grid(row=6, column=0)
        name_y.grid(row=6, column=1)
        name_z.grid(row=6, column=2)
        name_x_input.grid(row=7, column=0)
        name_y_input.grid(row=7, column=1)
        name_z_input.grid(row=7, column=2)
        new_file_button.grid(row=8, column=0, columnspan=4, pady=10)
        warning_.grid(row=9, column=0, columnspan=5)
        go_back_button.grid(row=10, column=0, columnspan=4)


class EditFunctionMenu(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        def create_table_if_not_exists():
            db_connection = sqlite3.connect("user_data.db")
            db_cursor = db_connection.cursor()
            db_cursor.execute("""CREATE TABLE IF NOT EXISTS file_data(
            username TEXT,
            filename TEXT,
            filetype TEXT,
            filepath TEXT,
            dimension TEXT,
            graphtype TEXT,
            xname TEXT,
            yname TEXT,
            zname TEXT 
             )""")
            db_connection.commit()
            db_connection.close()

        create_table_if_not_exists()

        def button_command():
            db_connection = sqlite3.connect("user_data.db")
            db_cursor = db_connection.cursor()
            db_cursor.execute("DELETE FROM file_data WHERE (filename=? AND username=?)",
                              (anchored_file_data[1], logged_username))
            db_connection.commit()
            db_cursor.execute("SELECT filename FROM file_data WHERE (filename=? AND username=?) ",
                                  (new_file_name_input.get(), logged_username))
            results = db_cursor.fetchall()
            if len(results) == 0:
                db_cursor.execute("INSERT INTO file_data VALUES(?,?,?,?,?,?,?,?,?)", (logged_username,
                                                                                      new_file_name_input.get(),
                                                                                      "function",
                                                                                      "",
                                                                                      "",
                                                                                      "",
                                                                                      name_x_input.get(),
                                                                                      name_y_input.get(),
                                                                                      ""
                                                                                      ))
                db_connection.commit()
                parent.show_frame(MainMenu)
            elif len(results) == 1:
                warning_.configure(text="Name of the function already exists")

        parent.geometry("500x300")
        new_file_name_label = tk.Label(self, text="Please give a name to the function:")
        name_x = tk.Label(self, text="Range of X values:"
                                     "\n(Enter like shown or errors will occur:"
                                     "\n(min,max,number of x values))")
        name_y = tk.Label(self, text="Function(y=?):")
        warning_ = tk.Label(self, text="")

        name_x_input = tk.Entry(self)
        name_x_input.insert(0, anchored_file_data[6])
        name_y_input = tk.Entry(self)
        name_y_input.insert(0, anchored_file_data[7])
        new_file_name_input = tk.Entry(self)
        new_file_name_input.insert(0, anchored_file_data[1])

        new_file_button = tk.Button(self, text="Add new function", command=lambda: button_command())
        go_back_button = tk.Button(self, text="Go Back", command=lambda: parent.show_frame(MainMenu))

        new_file_name_input.grid(row=0, column=1)
        new_file_name_label.grid(row=0, column=0)
        name_x.grid(row=2, column=0)
        name_y.grid(row=3, column=0)
        name_x_input.grid(row=2, column=1)
        name_y_input.grid(row=3, column=1)
        new_file_button.grid(row=4, column=0, columnspan=2, pady=10)
        warning_.grid(row=5, column=0, columnspan=2)
        go_back_button.grid(row=6, column=0, columnspan=2)


if __name__ == "__main__":
    app = Window()
    app.mainloop()
