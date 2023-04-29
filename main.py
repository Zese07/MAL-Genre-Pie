import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import requests


def pop_up(number):
    popup = tk.Toplevel()

    popup.title("Error" if number == 0 else "Done")

    popup.geometry("200x50+{}+{}".format(window.winfo_rootx() + window.winfo_width() // 2 - 110,
                                         window.winfo_rooty() + window.winfo_height() // 2 - 50))
    popup.iconbitmap('icon.ico')
    popup.resizable(False, False)

    text = tk.Label(popup, text="Unexpected error occurred." if number == 0 else "Pie graph successfully created.")

    text.pack()

    popup.after(1000 if number == 0 else 3000, popup.destroy)


def tier(percent):
    tiers = [(100, u'\u2605'), (96, 'S+'), (91, 'S'), (83, 'A+'), (76, 'A'), (68, 'B+'), (61, 'B'),
             (53, 'C+'), (46, 'C'), (38, 'D+'), (31, 'D'), (23, 'E+'), (16, 'E'), (8, 'F+'), (0, 'F')]

    for low, tier in tiers:
        if percent >= low:
            return tier

    return 'F'


def pie_chart(total, watching, completed, on_hold, dropped, plan_to_watch, genre_name, percent, center, color):
    total -= len(watching) + len(completed) + len(on_hold) + len(dropped) + len(plan_to_watch)
    numbers = [len(watching), len(completed), len(on_hold), len(dropped), len(plan_to_watch), total]
    labels = ['Watching', 'Completed', 'On-Hold', 'Dropped', 'Plan to Watch', 'Unexplored']
    colors = color

    figure, pie = plt.subplots(figsize=(5, 5))
    pie.pie(numbers, labels=None, colors=colors, startangle=90)

    center_circle = plt.Circle((0, 0), 0.7, fc=f'{colors[0]}')
    fig = plt.gcf()
    fig.gca().add_artist(center_circle)

    legend_labels = [f'{label}: {num}' for label, num in zip(labels, numbers)]
    pie.legend(legend_labels, loc='upper right', bbox_to_anchor=(1.0705, 0.75))
    figure.subplots_adjust(left=-0.25, bottom=0.25)

    pie.text(0, 0.075, f'{center}', ha='center', va='center', size=60, color=f'{colors[4]}')
    pie.text(0, -0.2, f'{round(percent, 3)}%', ha='center', va='center', size=10, color=f'{colors[3]}')
    pie.text(0, -0.325, f'{genre_name}', ha='center', va='center', size=9, color=f'{colors[4]}')
    pie.axis('equal')

    plt.savefig('pie.png')

    pop_up(1)


def pie_color(color):
    colors = {'Green': ['#ccffcc', '#80ff80', '#33ff33', '#00e600', '#009900', '#004d00'],
              'Blue': ['#cceeff', '#80d4ff', '#33bbff', '#0099e6', '#006699', '#00334d'],
              'Pink': ['#ffccff', '#ff80ff', '#ff33ff', '#e600e6', '#990099', '#4d004d'],
              'Red': ['#ffcccc', '#ff8080', '#ff3333', '#e60000', '#990000', '#4d0000'],
              'Orange': ['#ffe6cc', '#ffbf80', '#ff9933', '#e67300', '#994d00', '#4d2600'],
              'Yellow': ['#ffffcc', '#ffff80', '#ffff33', '#e6e600', '#999900', '#4d4d00']}

    return colors.get(color)


def submit():
    username = username_input.get()
    access = token_input.get()

    genres = {'Action': 1, 'Adventure': 2, 'Anthropomorphic': 51, 'Award Winning': 46, 'Avant Garde': 5, 'Boys Love': 28, 'CGDCT': 52,
              'Childcare': 53, 'Combat Sports': 54, 'Comedy': 4, 'Crossdressing': 81, 'Delinquents': 55, 'Detective': 39, 'Drama': 8,
              'Ecchi': 9, 'Educational': 56, 'Erotica': 49, 'Fantasy': 10, 'Gag Humor': 57, 'Girls Love': 26, 'Gore': 58,
              'Gourmet': 47, 'Harem': 35, 'Hentai': 12, 'High Stakes Game': 59, 'Historical': 13, 'Horror': 14, 'Idols (Female)': 60,
              'Idols (Male)': 61, 'Isekai': 62, 'Iyashikei': 63, 'Josei': 43, 'Kids': 15, 'Love Polygon': 64, 'Magical Sex Shift': 65,
              'Mahou Shoujo': 66, 'Martial Arts': 17, 'Mecha': 18, 'Medical': 67, 'Military': 38, 'Music': 19, 'Mythology': 6,
              'Organized Crime': 68, 'Otaku Culture': 69, 'Parody': 20, 'Performing Arts': 70, 'Pets': 71, 'Psychological': 40, 'Racing': 3,
              'Reincarnation': 72, 'Reverse Harem': 73, 'Romance': 22, 'Romantic Subtext': 74, 'Samurai': 21, 'School': 23, 'Sci-Fi': 24,
              'Seinen': 42, 'Shoujo': 25, 'Shounen': 27, 'Showbiz': 75, 'Slice of Life': 36, 'Space': 29, 'Sports': 30,
              'Strategy Game': 11, 'Super Power': 31, 'Supernatural': 37, 'Survival': 76, 'Suspense': 41, 'Team Sports': 77, 'Time Travel': 78,
              'Vampire': 32, 'Video Game': 79, 'Visual Arts': 80, 'Workplace': 48}

    genre_name = genre_combobox.get()
    genre_id = genres.get(genre_combobox.get(), 0)
    color = color_combobox.get()

    try:
        response = requests.get(f'https://api.myanimelist.net/v2/users/{username}/animelist')

        if response.status_code != 404:
            if ' ' in username:
                print("Should not have spaces.")
            else:
                response = requests.get(f'https://api.jikan.moe/v4/anime?genres={genre_id}')
                jikan = response.json()
                total = jikan['pagination']['items']['total']

                response = requests.get(f'https://api.jikan.moe/v4/users/{username}/statistics')
                mal = response.json()
                total_watching = int(mal['data']['anime']['watching'])
                total_completed = int(mal['data']['anime']['completed'])
                total_on_hold = int(mal['data']['anime']['on_hold'])
                total_dropped = int(mal['data']['anime']['dropped'])
                total_plan_to_watch = int(mal['data']['anime']['plan_to_watch'])
                stats = [total_watching, total_completed, total_on_hold, total_dropped, total_plan_to_watch]
                stats_name = ['watching', 'completed', 'on_hold', 'dropped', 'plan_to_watch']
                stats_loop = []

                for x in range(len(stats)):
                    loop = 1 if stats[x] % 1000 != 0 else 0
                    loop += int(stats[x] / 1000)
                    stats_loop.append(loop)

                watching, completed, on_hold, dropped, plan_to_watch = [], [], [], [], []
                stats_data = [watching, completed, on_hold, dropped, plan_to_watch]

                for y in range(len(stats)):
                    off = 0
                    for x in range(0, stats_loop[y]):
                        url = f"https://api.myanimelist.net/v2/users/{username}/animelist?status={stats_name[y]}&fields=genres,list_status&offset={off}&limit=1000"
                        headers = {"Authorization": f"Bearer {access}"}
                        response = requests.get(url, headers=headers)
                        mal = response.json()
                        for item in mal['data']:
                            off += 1
                            if 'node' in item and 'genres' in item['node']:
                                genres = item['node']['genres']
                                for genre in genres:
                                    if 'name' in genre and genre['name'] == genre_name:
                                        stats_data[y].append(item['node']['id'])
                                        break

                percent = (len(completed) / total) * 100
                center = tier(percent)
                color = pie_color(color)
                pie_chart(total, watching, completed, on_hold, dropped, plan_to_watch, genre_name, percent, center, color)

    except Exception:
        pop_up(0)


window = tk.Tk()
window.title("Genre Pie")
window.geometry("280x225+{}+{}".format((window.winfo_screenwidth() // 2) - (280 // 2),
                                       (window.winfo_screenheight() // 2) - (225 // 2)))
window.iconbitmap('icon.ico')
window.resizable(False, False)

username_label = ttk.Label(window, text="MAL Username:")
username_label.grid(row=0, column=0, padx=10, pady=10)
username_input = ttk.Entry(window)
username_input.grid(row=0, column=1, padx=10, pady=10)

token_label = ttk.Label(window, text="Access Token:")
token_label.grid(row=1, column=0, padx=10, pady=10)
token_input = ttk.Entry(window)
token_input.grid(row=1, column=1, padx=10, pady=10)

genre_label = ttk.Label(window, text="Anime Genre:")
genre_label.grid(row=2, column=0, padx=10, pady=10)
genre_combobox = ttk.Combobox(window, values=['Action', 'Adventure', 'Anthropomorphic', 'Award Winning', 'Avant Garde', 'Boys Love', 'CGDCT',
                                              'Childcare', 'Combat Sports', 'Comedy', 'Crossdressing', 'Delinquents', 'Detective', 'Drama',
                                              'Ecchi', 'Educational', 'Erotica', 'Fantasy', 'Gag Humor', 'Girls Love', 'Gore', 'Gourmet',
                                              'Harem', 'Hentai', 'High Stakes Game', 'Historical', 'Horror', 'Idols (Female)', 'Idols (Male)',
                                              'Isekai', 'Iyashikei', 'Josei', 'Kids', 'Love Polygon', 'Magical Sex Shift', 'Mahou Shoujo',
                                              'Martial Arts', 'Mecha', 'Medical', 'Military', 'Music', 'Mythology', 'Organized Crime',
                                              'Otaku Culture', 'Parody', 'Performing Arts', 'Pets', 'Psychological', 'Racing', 'Reincarnation',
                                              'Reverse Harem', 'Romance', 'Romantic Subtext', 'Samurai', 'School', 'Sci-Fi', 'Seinen', 'Shoujo',
                                              'Shounen', 'Showbiz', 'Slice of Life', 'Space', 'Sports', 'Strategy Game', 'Super Power',
                                              'Supernatural', 'Survival', 'Suspense', 'Team Sports', 'Time Travel', 'Vampire', 'Video Game',
                                              'Visual Arts', 'Workplace'], state='readonly')
genre_combobox.set('Action')
genre_combobox.grid(row=2, column=1, padx=10, pady=10)

color_label = ttk.Label(window, text="Pie Graph Color:")
color_label.grid(row=3, column=0, padx=10, pady=10)
color_combobox = ttk.Combobox(window, values=['Green', 'Blue', 'Pink', 'Red', 'Orange', 'Yellow'], state='readonly')
color_combobox.set('Green')
color_combobox.grid(row=3, column=1, padx=10, pady=10)

submit_button = ttk.Button(window, text="Submit", command=submit)
submit_button.grid(row=4, column=0, columnspan=2, pady=10)

window.mainloop()
