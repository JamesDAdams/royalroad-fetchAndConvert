from requests_html import HTMLSession
import sys
import time

#GNU GPLv3 License https://www.gnu.org/licenses/gpl-3.0.en.html




def main(next_url, nb_chapters, file_name, start_chapter=1, writeFile=True, logger=print):

    CSS='''<style>
    .chapter-content table {
        background: #004b7a;
        margin: 10px auto;
        width: 90%;
        border: none;
        box-shadow: 1px 1px 1px rgba(0,0,0,.75);
        border-collapse: separate;
        border-spacing: 2px;
    }
    .chapter-content table td {
        color: #ccc;
    }
    </style>
    '''

    logger("URL : ", next_url)
    logger("Number of chapters : ", nb_chapters)
    logger("Start from chapter : ", start_chapter)
    logger("File name : ", file_name, "\n")

    session = HTMLSession()
    if writeFile:
        f = open(file_name, "w+", encoding="utf-8")
        f.write(CSS)

    book = CSS
    chapter_count = 1
    while chapter_count <= nb_chapters:
        try:
            s = session.get(next_url)
            S = ""

            # Website implemented protection against scraping
            # "Slow down!"
            while(s.status_code == 429):
                time.sleep(0.2)
                s = session.get(next_url)

            if chapter_count >= start_chapter:
                #Fetch title
                chapter_title = (s.html.find('h1.font-white')[0]).text
                S += '<h1 class=\"chapter\">' + chapter_title + '</h1>\n'
                logger(chapter_count, " ", chapter_title)
                #Fetch the chapter content
                chapter_content = s.html.find('.chapter-inner', first=True).html
                S += chapter_content
                #Fetch the author note (if there is one)
                author_note = s.html.find('.portlet-body.author-note')
                if(len(author_note) == 1):
                    note_content = author_note[0].html
                    S += '<h3 class=\"author_note\"> Author note </h3>\n'
                    S += note_content
                elif(len(author_note) == 2):
                    note_content = author_note[0].html
                    S += '<h3 class=\"author_note\"> Author note top page </h3>\n'
                    S += note_content
                    note_content = author_note[1].html
                    S += '<h3 class=\"author_note\"> Author note bottom page </h3>\n'
                    S += note_content

                book += S
                if writeFile:
                    f.write(S)

            try:
                #Fetch the url of the next chapter
                next_url = "https://www.royalroad.com" + (s.html.find('[rel=next]')[0]).attrs.get("href")
            except:
                logger("Last chapter ! Exiting...")
                break

            chapter_count += 1

        except:
            logger("Error on chapter", chapter_count, sys.exc_info()[0])
            if writeFile:
                f.close()
            break

    f.close()
    return S

def printUsage():
    logger("Usage :\n   fetch_book.py url_of_chapter number_of_chapters [start_chapter] name_of_ebook")

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) not in (3, 4):
        printUsage()
        exit()

    next_url = args[0]
    nb_chapters = int(args[1])
    if len(args) == 4:
        start_chapter = int(args[2])
        file_name = args[3] + ".html"
    else:
        start_chapter = 1
        file_name = args[2] + ".html"
    main(next_url, nb_chapters, file_name, start_chapter)
    exit()