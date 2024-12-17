from bs4 import BeautifulSoup

class Parser1:
    def parse_schedule_page(self, schedule_page: str, faculty_names: tuple[str]):
        result = {}
        soup = BeautifulSoup(schedule_page, 'lxml')
        faculties = soup.find_all('div', class_ = 'faculty')
        for faculty_name in faculty_names:
            for faculty in faculties:
                if faculty_name in faculty.find('h4').text:
                    result[faculty_name] = {}
                    rows = faculty.find_all('tr')
                    for row in rows:
                        columns = row.find_all('td')
                        year = columns[0].text.split(' ')[0]
                        result[faculty_name][year] = {}
                        links = columns[1].find_all('a')
                        for link in links:
                            if 'а(' in link.text:
                                result[faculty_name][year][link.decode_contents()] = [link.get('href'), link.get('title'), 'Кадры высшей квалификации'] 
                            elif 'м' in link.text:
                                result[faculty_name][year][link.decode_contents()] = [link.get('href'), link.get('title'), 'Магистратура'] 
                            elif 'б' in link.text:
                                result[faculty_name][year][link.decode_contents()] = [link.get('href'), link.get('title'), 'Бакалавриат'] 
                            else:
                                result[faculty_name][year][link.decode_contents()] = [link.get('href'), link.get('title'), 'Специалитет'] 

        return result
