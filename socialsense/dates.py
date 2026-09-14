from datetime import date


MONTHS={ "January":1, "February":2, "March":3, "April":4, "May": 5, "June": 6,
         "July": 7, "August": 8, "September":9,"October":10, "November":11, "December":12}




def parse_dates(labels, start_year):
    """['september 10',...]-> [datetime,...]

    assumes that the rows are in chronological order,
    increments the year when the month goes backwards december->january.
    """
    result=[] #boş liste oluşturuyor
    year= start_year
    prev_month=None 


    for label in labels:
        name, day= label.split()
        month= MONTHS[name]


        #yıl kontrolü gelecek
        if prev_month is not None and month < prev_month:
            year += 1


        result.append(date(year,month, int(day)))
        prev_month= month


    return result


if __name__ == "__main__":
    test = ["December 30", "December 31", "January 1", "January 2"]
    for d in parse_dates(test, 2025):
        print(d)