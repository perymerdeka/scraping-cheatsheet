from bs4 import BeautifulSoup
# cheat for read and parsing HTML file

# using open func



with open('res.html') as file:
    soup = BeautifulSoup(file, 'html.parser')

    # scraping process
    title = soup.title.string
    print(title)

    # > Documents result


# option 2

file = open('res.html')
soup = BeautifulSoup(file, 'html.parser')
title = soup.title.string
print(title)

# > Documents result
