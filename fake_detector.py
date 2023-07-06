import csv, time, ast
import decision_support_system
import tkinter
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from selenium.common.exceptions import *
from selenium import webdriver
from pandas import read_csv as read
from tkinter import *
import tkinter as tk
import tkinter as Tk
from PIL import ImageTk, Image

class Scrapper:
    def __init__(self, person_id):
        self.person_id = person_id

    def get_avatar_info(self):
        try:
            main_photos = driver.find_element_by_css_selector(
                '#fbTimelineHeadline > div.name > div > div > a > img').get_attribute('alt')
            # print('Info about avatar: ' + str(main_photos))
        except NoSuchElementException:
            main_photos = 'No info about avatar'
            # print('No info about avatar')
            pass
        return main_photos

    def get_avatar_link(self):
        try:
            avatar_link = driver.find_element_by_css_selector(
                '#fbTimelineHeadline > div.name > div > div > a > img').get_attribute('src')
            # print('Avatar: ' + str(avatar_link))
        except NoSuchElementException:
            avatar_link = 'Avatar doesn`t exist'
            # print('Avatar doesn`t exist')
            pass
        return avatar_link

    def get_cover_info(self):
        try:
            info_about_photo = driver.find_element_by_css_selector('img.coverPhotoImg.photo.img').get_attribute('alt')
            # print('Info about cover: ' + str(info_about_photo))
        except NoSuchElementException:
            info_about_photo = 'No info about cover photo'
            # print('No info about cover photo')
            pass
        return info_about_photo

    def get_cover_link(self):
        try:
            cover_link = driver.find_element_by_css_selector('img.coverPhotoImg.photo.img').get_attribute('src')
            # print('Cover: ' + str(cover_link))
        except NoSuchElementException:
            cover_link = 'Cover photo doesn`t exist'
            # print('Cover photo doesn`t exist')
            pass
        return cover_link

    def get_intro_info(self):
        try:
            intro = driver.find_element_by_id('intro_container_id').text
            # print('Info about user: ' + intro)
        except NoSuchElementException:
            intro = 'No info about user'
            # print('No info about user')
            pass
        return intro

    def get_number_of_photos(self):
        try:
            photos = driver.find_element_by_xpath('//span[text()="Photos"]').click()
            time.sleep(2)
            # Get scroll height
            SCROLL_PAUSE_TIME = 2
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            photos_count = driver.find_elements_by_class_name('fbPhotoStarGridElement')
            # print('Number of photos: ' + str(len(photos_count)))
            photos_count = str(len(photos_count))
        except NoSuchElementException:
            photos_count = 'No info about photos'
            # print('No info about photos')
            pass
        return photos_count

    def get_number_of_posts(self):
        try:
            posts = driver.find_elements_by_class_name('profileLink')
            # print('Number of posts: ' + str(len(posts)))
            posts = str(len(posts))
        except NoSuchElementException:
            posts = 'No info about posts'
            # print('No info about posts')
            pass
        return posts

    def get_number_of_friends(self):
        try:
            friends = driver.find_element_by_css_selector(
                '#profile_timeline_tiles_unit_pagelets_friends > li > div > div > div > div > div > div > div > div > span:nth-child(3) > a').text
            # print('Number of friends: ' + str(friends))
        except NoSuchElementException:
            friends = 'No info about friends'
            # print('No info about friends')
            pass
        return friends

    def get_personal_info(self, person_id):
        driver.get(person_id + '/about')
        driver.find_element_by_tag_name('body').click()
        time.sleep(5)
        personal_info = driver.find_element_by_css_selector(
            '.uiList > li > div > div:nth-child(2) > div > div > div:nth-child(1)').text
        # print('========================================\nWork, education, living, relationship info: \n' + personal_info)
        return personal_info

    def get_contacts_and_birthday(self):
        try:
            contacts_and_birthday = driver.find_element_by_css_selector(
                '.uiList > li > div > div:nth-child(2) > div > div > div:nth-child(2)').text

            birthday = re.findall('\d{2} [a-zA-Z]{3,9} \d{4}', contacts_and_birthday)
            # print(birthday)
            if birthday != []:
                birthday = birthday[0]
            else:
                birthday = 'No info about birthday'
                # print('No info about birthday')

            try:
                contacts_and_birthday = contacts_and_birthday.replace('\n', '.')
                contacts = re.search('%s(.*)%s' % ('Social Links.', '.Birthday'), contacts_and_birthday).group(1)
                contacts = contacts.replace('.', '\n')
            except AttributeError:
                contacts = 'No contacts'
                # print('*******************************************')
                # print(birthday)
                # print(contacts)
                # print('*******************************************')
        except NoSuchElementException:
            contacts = 'The "Contacts" container is empty'
            birthday = 'The "Birthday" container is empty'
            # print('The "Contacts" container is empty')
            pass
        return birthday, contacts

    def get_avatar_likes_and_comments(self):
        try:
            driver.find_element_by_css_selector('.name .photoContainer > div > a').click()
            time.sleep(3)
            try:
                likes_on_avatar = driver.find_element_by_css_selector(
                    '.fbPhotosSnowliftFeedbackForm > div:nth-child(4) > div > div > div:nth-child(1) > div:nth-child(1)').text
                likes_on_avatar = re.findall(r'^\w*', likes_on_avatar)
                likes_on_avatar = int(likes_on_avatar[0])
                # print('Number of likes: ' + str(likes_on_avatar[0]))

                people = driver.find_element_by_css_selector(
                    '.fbPhotosSnowliftFeedbackForm > div:nth-child(4) > div > div > div:nth-child(1) > div:nth-child(1)').text
            except:
                likes_on_avatar = 'No likes'
                # print('No likes')
                pass
            try:
                comments_on_avatar = driver.find_element_by_css_selector(
                    '.fbPhotosSnowliftFeedbackForm > div:nth-child(4) > div > div > div:nth-child(1) > div:nth-child(3)').text
                # print('Number of comments: ' + comments_on_avatar)
                comments_on_avatar = re.findall(r'^\w*', comments_on_avatar)
                if comments_on_avatar == ['']:
                    comments_on_avatar = 'No comments'
                else:
                    comments_on_avatar = comments_on_avatar[0]
            except:
                comments_on_avatar = 'No comments'
                # print('No comments')
                pass
        except:
            likes_on_avatar = 'No likes'
            comments_on_avatar = 'No comments'
        return likes_on_avatar, comments_on_avatar

    def get_people_liked_the_avatar(self):
        try:
            driver.find_element_by_css_selector(
                '.fbPhotosSnowliftFeedbackForm > div:nth-child(4) > div > div > div:nth-child(1) > div:nth-child(1) > a:nth-child(2)').click()
            # people_liked_the_avatar = driver.find_element_by_id('reaction_profile_browser1').text
            time.sleep(2)
            people_liked_the_avatar = driver.find_element_by_css_selector('.uiScrollableAreaContent > div > ul').text
            # people_liked_the_avatar = driver.find_element_by_class_name('uiList _4kg').text
            people_liked_the_avatar = people_liked_the_avatar.replace('Add Friend\n', '')
            people_liked_the_avatar = people_liked_the_avatar.replace('Add Friend', '')
            people_liked_the_avatar = people_liked_the_avatar.split('\n')
            # print(people_liked_the_avatar)
        except NoSuchElementException:
            people_liked_the_avatar = 'No likes on avatar'
        return people_liked_the_avatar

    def get_friends_list(self, person_id):
        driver.get(person_id + '/friends')
        time.sleep(2)
        driver.find_element_by_tag_name('body').click()
        SCROLL_PAUSE_TIME = 2
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        friends_list = driver.find_element_by_id('pagelet_timeline_medley_friends').text
        friends_list = friends_list.replace('Add Friend\n', '')
        friends_list = friends_list.split('\n')
        # print(friends_list)
        return friends_list

    def get_full_name(self):
        data_fullname = driver.find_element_by_css_selector('#fb-timeline-cover-name > a').text
        # print('Full name: ' + data_fullname)
        return data_fullname

    def get_number_of_friends_and_strangers_likes(self, people_liked_the_avatar, likes_on_avatar, friend_list):
        people_liked_the_avatar = people_liked_the_avatar
        likes_on_avatar = likes_on_avatar
        friend_list = friend_list

        if people_liked_the_avatar != 'No likes on avatar':
            friends_liked_the_avatar = list(set(friend_list) & set(people_liked_the_avatar))
            number_of_fiends_liked_the_avatar = int(len(friends_liked_the_avatar))
            number_of_strangers_liked_the_avatar = likes_on_avatar - number_of_fiends_liked_the_avatar
            number_of_likes_on_avatar = {}
            number_of_likes_on_avatar['Number of friends` likes: '] = number_of_fiends_liked_the_avatar
            number_of_likes_on_avatar['Number of strangers` likes: '] = number_of_strangers_liked_the_avatar
        else:
            number_of_likes_on_avatar = 'No info about likes on avatar'
        return number_of_likes_on_avatar

    def scrap(self, person_id):
        self.person_id = person_id

        driver.get(person_id)
        time.sleep(2)
        driver.find_element_by_tag_name('body').click()
        likes_on_avatar, comments_on_avatar = self.get_avatar_likes_and_comments()
        people_liked_the_avatar = self.get_people_liked_the_avatar()

        driver.get(person_id)
        time.sleep(2)
        driver.find_element_by_tag_name('body').click()

        # scroll = driver.find_element_by_tag_name('body')
        # scroll.send_keys(Keys.PAGE_DOWN)
        time.sleep(3)
        SCROLL_PAUSE_TIME = 2

        # Getting user`s full name

        full_name = self.get_full_name()

        # Getting info about avatar
        avatar_info = self.get_avatar_info()

        # Getting link on avatar
        avatar_link = self.get_avatar_link()

        # Getting info about cover
        cover_info = self.get_cover_info()

        # Getting link on cover
        cover_link = self.get_cover_link()

        # Getting info from intro container
        intro_info = self.get_intro_info()

        time.sleep(2)

        # ---NEEDS MODIFICATION BY ADDING SCROLL---
        # Getting number of user`s photo
        number_of_photos = self.get_number_of_photos()

        driver.get(person_id)
        time.sleep(2)
        driver.find_element_by_tag_name('body').click()

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Getting number of posts
        number_of_posts = self.get_number_of_posts()

        time.sleep(2)

        # Getting number of user`s friends
        number_of_friends = self.get_number_of_friends()

        # Getting personal info about user
        personal_info = self.get_personal_info(person_id)

        # Getting user contact information and birthday
        birthday, contacts = self.get_contacts_and_birthday()

        friend_list = self.get_friends_list(person_id)

        get_number_of_friends_and_strangers_likes = self.get_number_of_friends_and_strangers_likes(
            people_liked_the_avatar, likes_on_avatar, friend_list)

        print('\n\n')

        arr = []
        arr.append(str(full_name))
        arr.append(str(avatar_info))
        arr.append(str(avatar_link))
        arr.append(str(likes_on_avatar))
        arr.append(str(get_number_of_friends_and_strangers_likes))
        arr.append(str(people_liked_the_avatar))
        arr.append(str(comments_on_avatar))
        arr.append(str(cover_info))
        arr.append(str(cover_link))
        arr.append(str(intro_info))
        arr.append(str(number_of_photos))
        arr.append(str(number_of_posts))
        arr.append(str(number_of_friends))
        arr.append(str(friend_list))
        arr.append(str(personal_info))
        arr.append(str(birthday))
        arr.append(str(contacts))
        print(arr)

        with open('total.csv', "a", newline='', encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
            writer.writerow(arr)

        return arr

class Analyzer(Scrapper):
    def __init__(self, person_id):
        self.person_id = person_id

    def tonumber(self, person_id):
        data = Scrapper.scrap(self, person_id)
        # AVATAR P1
        if 'oh=cfbb962aa7a58f425d07881def1ebc01&oe=5E7215E0' in str(
                data[2]) or 'oh=794bea5187e612775f8b753766129863&oe=5E7FD7F3' in str(data[2]):
            self.P1 = 2
        elif 'person' in str(data[1]):
            self.P1 = 0
        else:
            self.P1 = 1

        # COVER P2
        if str(data[7]) == 'No info about cover photo':
            self.P2 = 2
        else:
            self.P2 = 0

        # PHOTOS P3
        if str(data[10]) == 'No info about photos':
            self.P3 = 2
        elif int(str(data[10]).replace(',', '')) < 10 or int(str(data[10]).replace(',', '')) > 1000:
            self.P3 = 1
        else:
            self.P3 = 0

        # FRIENDS P4
        if str(data[12]) == 'No info about friends':
            self.P4 = 2
        elif int(str(data[12]).replace(',', '')) < 10 or int(str(data[12]).replace(',', '')) > 2000:
            self.P4 = 1
        else:
            self.P4 = 0

        # POSTS P5
        if str(data[11]) == 'No info about posts':
            self.P5 = 2
        elif int(data[11]) < 10 or int(data[11]) > 500:
            self.P5 = 1
        else:
            self.P5 = 0

        # PERSONAL INFO P6
        if str(data[
                   14]) == 'No workplaces to show\nNo schools / universities to show\nNo places to show\nNo relationship info to show':
            self.P6 = 2
        elif 'No ' in str(data[14]):
            self.P6 = 1
        else:
            self.P6 = 0

        # CONTACTS AND BIRTHDAY P7
        if str(data[16]) == 'The "Contacts" container is empty' or str(data[16]) == 'No contacts':
            self.P7 = 2
        else:
            self.P7 = 0

        # P8
        if str(data[15]) == 'The "Birthday" container is empty' or str(data[15]) == 'No info about birthday':
            self.P8 = 2
        elif int(str(str(data[15])[-4:])) > 2009 or int(str(str(data[15])[-4:])) < 1932:
            self.P8 = 1
        else:
            self.P8 = 0

        # AVATAR LIKES AND COMMENTS P10
        if str(data[6]) == 'No comments':
            self.P10 = 2
        elif int(data[6]) < 5 or int(data[6]) > 100:
            self.P10 = 1
        else:
            self.P10 = 0

        # LIKES ON AVATAR P9
        if str(data[5]) == 'No likes on avatar' or str(data[5]) == 'No info about likes on avatar':
            self.P9 = 2
        elif int(ast.literal_eval(str(data[4]))['Number of friends` likes: ']) < int(
                ast.literal_eval(str(data[4]))['Number of strangers` likes: ']):
            self.P9 = 1
        else:
            self.P9 = 0

        return self.P1, self.P2, self.P3, self.P4, self.P5, self.P6, self.P7, self.P8, self.P9, self.P10

    def analyze(self, person_id):
        P1, P2, P3, P4, P5, P6, P7, P8, P9, P10 = self.tonumber(person_id)
        with open('account.csv', "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10'])
            writer.writerow(
                [str(person_id), str(P1), str(P2), str(P3), str(P4), str(P5), str(P6), str(P7), str(P8), str(P9),
                 str(P10)])

class GUI:
    def __init__(self):
        root = tk.Tk()

        root.resizable(width=True, height=True)
        root.title("Fake detector for Facebook v1.0")

        root.bind_all("<Key>", self.paste, "+")

        frame_info = Frame(root)
        frame_progressbar = Frame(root, bd=5)
        frame_status = Frame(root, bd=5)
        self.frame_graph = Frame(root, bd=5)

        label_id = Label(frame_status, font='TimesNewRoman 14')
        label_id['text'] = "User id:"
        label_id.pack()

        self.id_entry = Entry(frame_status, font='TimesNewRoman 14', width=25, borderwidth=1, justify=CENTER)
        self.id_entry.pack()

        check_button = Button(frame_info, width=15, height=5, fg="black", font='TimesNewRoman 14',
                              command=self.check_account)
        check_button["text"] = "Check page"
        check_button.bind("Check page")
        check_button.pack()

        label_status = Label(frame_status, font='TimesNewRoman 14')
        label_status['text'] = "Status: "
        label_status.pack()

        self.status_entry = Text(frame_status, height=1, width=17, font='Consolas 12')
        self.status_entry.pack()

        # LEGEND
        im = Image.open('Legend.jpg')
        tkimage = ImageTk.PhotoImage(im)
        label_image = tkinter.Label(self.frame_graph, image=tkimage)
        label_image.config(height=294, width=200)
        label_image.pack(side=RIGHT)

        frame_info.pack()
        frame_progressbar.pack()
        frame_status.pack()
        self.frame_graph.pack()
        root.mainloop()

    def check_account(self):
        person_id = str('https://www.facebook.com/' + self.id_entry.get())
        print(person_id)
        login = 'n00basya@mail.ru'
        password = '1234nubasik1234'
        driver.get("https://www.facebook.com")
        driver.find_element_by_name('email').send_keys(login)
        driver.find_element_by_name('pass').send_keys(password)

        try:
            driver.find_element_by_id('loginbutton').click()
        except:
            driver.find_element_by_name('login').click()
        time.sleep(2)

        analyzer = Analyzer(person_id)
        analyzer.analyze(person_id)
        result = self.histogram()
        print(result)

    def paste(self, event):
        ctrl = (event.state & 0x4) != 0
        if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
            event.widget.event_generate("<<Paste>>")

    def histogram(self):
        res = decision_support_system.NeuralNetwork()
        result = res.prediction()

        # Histogram
        figure = Figure(figsize=(6, 3), dpi=100)
        ax = figure.add_subplot(111)

        objects = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')

        data_file = read("account.csv", delimiter=",").head()
        mas = str(data_file.values[::, 1:11])
        mas = mas.replace('[', '')
        mas = mas.replace(']', '')
        mas = mas.split(' ')
        print(mas)
        mas = list(mas)
        i = 0
        while i < len(mas):
            mas[i] = int(mas[i])
            i+=1

        barchart = ax.bar(objects, mas, align='center', alpha=0.5, bottom=0)
        barchart[0].set_color('orange')
        barchart[1].set_color('orange')
        barchart[2].set_color('green')
        barchart[3].set_color('green')
        barchart[4].set_color('green')
        barchart[5].set_color('blue')
        barchart[6].set_color('blue')
        barchart[7].set_color('blue')
        barchart[8].set_color('red')
        barchart[9].set_color('red')

        ax.set_xticks(np.arange(len(objects)))
        ax.set_xticklabels(objects, fontdict=None, minor=False)

        y_labels = (0, 1, 2)
        ax.set_yticks(y_labels)
        ax.set_yticklabels(y_labels, fontdict=None, minor=False)

        ax.yaxis.grid()

        canvas = FigureCanvasTkAgg(figure, master=self.frame_graph)

        canvas.draw()
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        if result == 'Real':
            self.status_entry.insert(1.0, "The page is real")
            self.status_entry.tag_add("here", "1.0", "1.64")
            self.status_entry.tag_config("here", foreground="green")
        elif result == 'Fake':
            self.status_entry.insert(1.0, "The page is fake")
            self.status_entry.tag_add("here", "1.0", "1.64")
            self.status_entry.tag_config("here", foreground="red")
        return result

driver = webdriver.Chrome()
gui = GUI()
driver.close()