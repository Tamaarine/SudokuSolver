from selenium import webdriver
from typing import List

web_link = 'https://www.websudoku.com/'
browser = webdriver.Chrome()

def go_to_link():
    # Opens the link and max the window
    browser.get(web_link)

# Algorithm that solves sudoku
def solve(gameboard: List[List]) -> bool:
    for r in range(0, 9):
        for c in range(0, 9):
            if gameboard[r][c] == 0:
                for k in range(1,10):
                    gameboard[r][c] = k

                    if isValid(gameboard, r, c) and solve(gameboard):
                        return True

                    gameboard[r][c] = 0

                return False

    return True

def isValid(gameboard, row, col):
    return checkRow(gameboard, row) and checkCol(gameboard, col) and checkSubsquare(gameboard, row, col)

def checkCol(gameboard, column):
    nums = []
    determinant = []
    for i in range(0, 9):
        nums.append(False)
        determinant.append(False)

    for k in range(0, 9):
        determinant[k] = checkNumber(gameboard, k, nums, column)

    if all(determinant):
        return True
    else:
        return False

def checkRow(gameboard, row):
    nums = []
    determinant = []
    for i in range(0, 9):
        nums.append(False)
        determinant.append(False)

    for k in range(0, 9):
        determinant[k] = checkNumber(gameboard, row, nums, k)

    if all(determinant):
        return True
    else:
        return False

def checkSubsquare(gameboard, row, col):
    nums = []
    for i in range(0,9):
        nums.append(False)

    squareRowStart = (row//3) * 3
    squareRowEnd = squareRowStart + 3

    squareColStart = (col//3) * 3
    squareColEnd = squareColStart + 3

    for r in range(squareRowStart, squareRowEnd):
        for c in range(squareColStart, squareColEnd):
            if not checkNumber(gameboard, r, nums, c):
                return False

    return True

def checkNumber(gameboard, row, comparing, col):
    if gameboard[row][col] != 0:
        if not comparing[gameboard[row][col]-1]:
            comparing[gameboard[row][col]-1] = True
        else:
            return False

    return True

def switch_frame():
    # This site is a little weird since it use another frame
    # This gets the frame that is inside another frame and switch to it
    browser.switch_to.default_content()
    frame = browser.find_element_by_tag_name("frame")
    browser.switch_to.frame(frame)

def find_grid():

    # Constructing our 2D array. Length is 9
    sudoku = [[],[],[],[],[],[],[],[],[]]

    # Then we can just get the whole table element
    grid = browser.find_element_by_id("puzzle_grid")

    # Then we get each rows
    rows = grid.find_elements_by_tag_name("tr")

    for row in range(len(rows)):
        tds = rows[row].find_elements_by_tag_name("td")

        for td in range(len(tds)):

            determinant = tds[td].find_element_by_tag_name("input")
            # It is a empty cell
            if determinant.get_attribute("class") == "d0":
                # Here we are gathering datas
                sudoku[row].append(0)
            # Non-empty cell
            else:
                sudoku[row].append(0)
                sudoku[row][td] = int(determinant.get_attribute("value"))

    print("Problem")
    printBoard(sudoku)
    solve(sudoku)
    print("Solution")
    printBoard(sudoku)

    for row in range(len(rows)):
        tds = rows[row].find_elements_by_tag_name("td")

        for td in range(len(tds)):

            determinant = tds[td].find_element_by_tag_name("input")
            # It is a empty cell
            if determinant.get_attribute("class") == "d0":
                # Here we are gathering datas
                determinant.send_keys(str(sudoku[row][td]))

    # Submitting the answer
    submit = browser.find_element_by_xpath("//input[@name='submit']")
    submit.click()

    # Find the restart button
    restart = browser.find_element_by_name("newgame")
    restart.click()

def printBoard(gameboard):
    for row in range(0,9):
        for col in range(0,9):
            print(gameboard[row][col], end=" ")
        print()

if __name__ == '__main__':
    go_to_link()

    # Main loop that does the work
    while True:
        switch_frame()
        find_grid()
