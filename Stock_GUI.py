from __future__ import annotations

import Stock

import csv

import os

from tkinter import Frame, Label, Tk, Entry, N, S, W, E, VERTICAL, BOTH, \
    PhotoImage, Button, Menu, Scrollbar, END, Toplevel, Text
from tkinter.ttk import Notebook, Treeview, Style
from tkinter.messagebox import *
from tkinter import font
from Stock_Market_Calculations import convert_float_to_comma_sep_number

ACCOUNTS = 'Accounts.csv'
ACCOUNTS_HEADING = ('账号', '备注', '股票表格', '历史记录', '储蓄记录')
ACCOUNTS_COL = (150, 180, 90, 90, 90)

HEADING = ('股票名称', '市价', '持股数', '成本价', '市值', '浮动盈亏', '历史盈亏')
HISTORY_HEADER = ('操作日期', '操作内容', '备注')
# CSV_NAME = 'New Microsoft Excel Worksheet.csv'
# TXT_NAME = 'New Text Document.txt'
# HISTORY_NAME = 'History.csv'


Account = {'username': None, 'note': None, 'csv': None, 'history': None,
           'txt': None}

logout = [True]

# Login


def account_win(toplevel=False):
    if toplevel:
        account = Toplevel()
    else:
        account = Tk()
    account.title('账号登录')
    account.iconbitmap('Cui.ico')

    Lg = PhotoImage(file='CUI-stock.gif')
    Label(account, image=Lg).grid(row=0, columnspan=4)  # Title pic

    accounts_tab = Treeview(account, columns=ACCOUNTS_HEADING[0:2],
                            show='headings')
    scrbar = Scrollbar(account, orient=VERTICAL, command=accounts_tab.yview,
                       width=12)
    accounts_tab.configure(yscrollcommand=scrbar.set)

    for i in range(2):
        accounts_tab.column(ACCOUNTS_HEADING[i], width=ACCOUNTS_COL[i],
                            anchor='center')
        accounts_tab.heading(ACCOUNTS_HEADING[i], text=ACCOUNTS_HEADING[i])

    def account_refresh():
        for item in accounts_tab.get_children():
            accounts_tab.delete(item)

        with open(ACCOUNTS, 'r', encoding='UTF-8-sig') as f:
            all_users = csv.reader(f)
            f.readline()
            for line in all_users:
                displayed = [line[0]]
                limit_note = ''
                for ch in line[1]:
                    if len(limit_note) >= 8:
                        break
                    if ch == '\n':
                        break
                    limit_note += ch
                displayed.append(limit_note)
                accounts_tab.insert('', 'end', values=tuple(displayed))

    def login():
        selected = False
        for item in accounts_tab.selection():
            Account['username'] = accounts_tab.item(item, 'values')[0]
            selected = True

        with open(ACCOUNTS, 'r', encoding='UTF-8-sig') as f:
            all_users = csv.reader(f)
            f.readline()
            for line in all_users:
                if line[0] == Account['username']:
                    Account['note'] = line[1]
                    Account['csv'] = line[2]
                    Account['history'] = line[3]
                    Account['txt'] = line[4]
                    break

        if selected:
            logout[0] = False
            # account.iconify()
            account.quit()
            account.destroy()

    def login2(event):
        login()

    def new():
        new_win = Toplevel()
        NameLab = Label(new_win, text='账号名：')
        NameEntry = Entry(new_win)
        NoteLab = Label(new_win, text='备注：')
        NoteEntry = Entry(new_win)

        def create():
            if NameEntry.get() == '':
                return

            with open(ACCOUNTS, 'r', encoding='UTF-8-sig') as f:
                all_users = csv.reader(f)
                f.readline()
                for line in all_users:
                    if NameEntry.get().upper() == line[0].upper():
                        showerror('重复名称', '账户名已存在')
                        return

            csv_name = NameEntry.get() + '.csv'
            history_name = NameEntry.get() + '_history.csv'
            txt_name = NameEntry.get() + '.txt'
            with open(csv_name, 'w', encoding='UTF-8-sig', newline='') as o:
                f = csv.writer(o)
                f.writerow(HEADING)
            with open(history_name, 'w', encoding='UTF-8-sig', newline='') as o:
                f = csv.writer(o)
                f.writerow(HISTORY_HEADER)
            with open(txt_name, 'w', encoding='UTF-8-sig') as o:
                o.write('0.00\n0.00\n0.001')

            a = open(ACCOUNTS, 'a', newline='', encoding='UTF-8-sig')
            account_write = csv.writer(a)
            new_account = [NameEntry.get(), NoteEntry.get(), csv_name,
                           history_name,
                           txt_name]
            account_write.writerow(new_account)
            a.close()

            account_refresh()

            # new_win.quit()
            new_win.destroy()

        NameLab.grid(row=0)
        NameEntry.grid(row=0, column=1)
        NoteLab.grid(row=1)
        NoteEntry.grid(row=1, column=1)

        Button(new_win, text='创建账号', command=create).grid(row=2, columnspan=2)
        # new_win.mainloop()

    def delete_user():
        selected = False
        for item in accounts_tab.selection():
            username = accounts_tab.item(item, 'values')[0]
            note = accounts_tab.item(item, 'values')[1]
            selected = True
        with open(ACCOUNTS, 'r', encoding='UTF-8-sig') as f:
            all_users = csv.reader(f)
            f.readline()
            for line in all_users:
                if line[0] == username:
                    chart = line[2]
                    history = line[3]
                    txt = line[4]

        if selected:
            if not askokcancel('确认', '确认删除 {} ？'.format(username)):
                return

            f = open(ACCOUNTS, 'r', encoding='UTF-8-sig')
            users_read = csv.reader(f)

            new_file = []
            for line in users_read:
                if username == line[0]:
                    continue
                new_file.append(line)
            f.close()

            w = open(ACCOUNTS, 'w', newline='', encoding='UTF-8-sig')
            users_write = csv.writer(w)
            for line in new_file:
                users_write.writerow(line)
            w.close()

            os.remove(chart)
            os.remove(history)
            os.remove(txt)

            account_refresh()

    accounts_tab.bind('<Double-1>', login2)

    Button(account, text='登录账号', command=login, font=('Times', 10)).grid(row=2,
                                                                         column=1,
                                                                         pady=(
                                                                             7,
                                                                             7))
    Button(account, text='新账号', command=new, font=('Times', 10)).grid(row=2,
                                                                      column=0)
    Button(account, text='删除账号', command=delete_user, font=('Times', 10)).grid(
        row=2, column=2)
    accounts_tab.grid(row=1, column=0, columnspan=3, padx=(15, 0))
    scrbar.grid(row=1, column=3, sticky=N + S, padx=(0, 6))

    account_refresh()

    account.mainloop()


# 账户选择界面

account_win()

# 进入程序


while not logout[0]:
    logout[0] = True

    User = Stock.TotalAssets(Account['csv'], Account['txt'], Account['history'],
                             name=Account['username'])

    # GUI初始设置
    root = Tk()
    root.title('CUi 股票管理系统')
    root.iconbitmap('Cui.ico')

    Style().element_create('Plain.Notebook.tab', 'from', 'default')
    Style().layout('TNotebook.Tab', [('Plain.Notebook.tab', {'children': [(
        'Notebook.padding',
        {
            'side': 'top',
            'children': [
                (
                    'Notebook.focus',
                    {
                        'side': 'top',
                        'children': [
                            (
                                'Notebook.label',
                                {
                                    'side': 'top',
                                    'sticky': ''})],
                        'sticky': 'nswe'})],
            'sticky': 'nswe'})],
        'sticky': 'nswe'})])
    Style().layout('TNotebook1.Tab', [('Plain.Notebook.tab', {'children': [(
        'Notebook.padding',
        {
            'side': 'top',
            'children': [
                (
                    'Notebook.focus',
                    {
                        'side': 'top',
                        'children': [
                            (
                                'Notebook.label',
                                {
                                    'side': 'top',
                                    'sticky': ''})],
                        'sticky': 'nswe'})],
            'sticky': 'nswe'})],
        'sticky': 'nswe'})])

    bg_color = 'white'

    ft1 = font.Font(family='Times', size=25, weight=font.BOLD)
    ft2 = font.Font(family='Helvetica', size=25, weight=font.NORMAL)
    ft3 = font.Font(family='Times', size=15, weight=font.NORMAL)

    Style().configure('TNotebook.Tab', padding=[80, 3], borderwidth=2, font=ft3)
    Style().map('TNotebook.Tab', background=[('selected', bg_color)])

    Style().configure('Treeview.Heading', font=('Verdana', 12))

    WIDTH = root.winfo_screenwidth() - 150
    HEIGHT = root.winfo_screenheight() - 100
    X = (root.winfo_screenwidth() - WIDTH) // 2
    Y = (root.winfo_screenheight() - HEIGHT) // 2
    # print(root.winfo_screenwidth())

    COL_WID = (145, 105, 105, 105, 105, 105, 105)
    HISTORY_COL_WID = (120, 220, 150)

    root.geometry('{}x{}+{}+{}'.format(WIDTH, HEIGHT, X, Y))

    # 设置标签页的基本框架
    OverallPage = Notebook(root, padding=10)

    DealFrame = Frame(OverallPage)
    DepositFrame = Frame(OverallPage)
    ShareFrame = Frame(OverallPage)

    DealPage = Notebook(DealFrame)
    DepositPage = Notebook(DepositFrame, height=152)
    SharePage = Notebook(ShareFrame, height=152)

    BuyFrame = Frame(DealPage)
    SellFrame = Frame(DealPage)
    RecordFrame = Frame(DealPage)

    IncomeFrame = Frame(DepositPage)
    ExpenseFrame = Frame(DepositPage)

    CashShareFrame = Frame(SharePage)
    StockShareFrame = Frame(SharePage)

    DealPage.add(BuyFrame, text='买入', sticky='n')
    DealPage.add(SellFrame, text='卖出', sticky='n')
    DealPage.add(RecordFrame, text='记录市价', sticky='n')

    DepositPage.add(IncomeFrame, text='         存款      ', sticky='n')
    DepositPage.add(ExpenseFrame, text='      取款        ', sticky='n')

    SharePage.add(CashShareFrame, text='       分股息       ', sticky='n')
    SharePage.add(StockShareFrame, text='       分红股       ', sticky='n')

    OverallPage.add(DealFrame, text='交易', sticky='n')
    OverallPage.add(DepositFrame, text='存取款', sticky='n')
    OverallPage.add(ShareFrame, text='分红', sticky='n')

    TableFrame = Frame(root)
    HistoryFrame = Frame(root)
    DataFrame = Frame(root)

    Logo = PhotoImage(file='CUI-stock.gif')
    TitleFrame1 = Frame(root, height=10)
    TitleFrame2 = Frame(root, height=20)
    Title = Label(root, image=Logo)

    Label(TitleFrame2, text='登录账户：' + User.name, font=ft3).grid(row=0)

    # 放置标签页
    DealPage.pack(fill=BOTH)
    DepositPage.pack(fill=BOTH)
    SharePage.pack()
    # OverallPage.pack()
    # TitleFrame1.grid(row=0, columnspan=2)
    Title.grid(row=1, columnspan=2, sticky=N + S)
    TitleFrame2.grid(row=2, columnspan=2)
    OverallPage.grid(row=3, column=1, sticky=N)
    TableFrame.grid(row=3, column=0, rowspan=3, sticky=N + S)
    DataFrame.grid(row=4, column=1, sticky=N)
    HistoryFrame.grid(row=5, column=1, sticky=N)
    # TableFrame.pack()

    # 初始化内部程序

    # 设置交易标签页的内容

    # 买入的页面
    # BuyDateLab = Label(BuyFrame, text='date', width=25)
    BuyNameLab = Label(BuyFrame, text='股票名称', font=ft3)
    BuyPriceLab = Label(BuyFrame, text='交易价格', font=ft3)
    BuyNumLab = Label(BuyFrame, text='交易数量', font=ft3)
    BuyNoteLab = Label(BuyFrame, text='备注', font=ft3)

    # BuyDateEntry = Entry(BuyFrame, width=30)
    BuyNameEntry = Entry(BuyFrame, font=(None, 11))
    BuyPriceEntry = Entry(BuyFrame, font=(None, 11))
    BuyNumEntry = Entry(BuyFrame, font=(None, 11))
    BuyNoteEntry = Entry(BuyFrame, font=(None, 11))


    # 买入执行程序

    def buy():
        try:
            num = int(BuyNumEntry.get())
            price = float(BuyPriceEntry.get())
        except ValueError:
            showerror('输入不合法', '请输入数字')
            return
        name = BuyNameEntry.get()
        if name == '':
            showerror('缺少名称', '请输入名称')
            return
        error = User.buy_stock(name, num, price, BuyNoteEntry.get())
        if error is not None:
            showerror(error, '存款不够')
            return
        confirm = askokcancel('交易确认',
                              '你即将以{}元每股的价钱买入{} {}股。共计花费{}元'.format(price, name,
                                                                    num,
                                                                    price * num))
        if confirm:
            update_table()
            update_history()


    # 买入按钮
    BuyButton = Button(BuyFrame, text='买入', command=buy, font=ft3)

    # 卖出的页面
    # SellDateLab = Label(SellFrame, text='date')
    SellNameLab = Label(SellFrame, text='股票名称', font=ft3)
    SellPriceLab = Label(SellFrame, text='交易价格', font=ft3)
    SellNumLab = Label(SellFrame, text='交易数量', font=ft3)
    SellNoteLab = Label(SellFrame, text='备注', font=ft3)

    # SellDateEntry = Entry(SellFrame)
    SellNameEntry = Entry(SellFrame, font=(None, 11))
    SellPriceEntry = Entry(SellFrame, font=(None, 11))
    SellNumEntry = Entry(SellFrame, font=(None, 11))
    SellNoteEntry = Entry(SellFrame, font=(None, 11))


    # 卖出执行程序

    def sell():
        try:
            num = int(SellNumEntry.get())
            price = float(SellPriceEntry.get())
        except ValueError:
            showerror('输入不合法', '请输入数字')
            return
        name = SellNameEntry.get()
        if name == '':
            showerror('缺少名称', '请输入名称')
            return
        error = User.sell_stock(name, num, price, SellNoteEntry.get())
        if error is not None:
            showerror(error, '股票不存在或您的持股数小于您的卖出量')
            return
        confirm = askokcancel('交易确认',
                              '你即将以{}元每股的价钱卖出{} {}股。共计收入{}元'.format(price, name,
                                                                    num,
                                                                    price * num))
        if confirm:
            update_table()
            update_history()


    # 卖出按钮
    SellButton = Button(SellFrame, text='卖出', command=sell, font=ft3)

    # 记录市价的页面
    # RecordDateLab = Label(RecordFrame, text='date')
    RecordNameLab = Label(RecordFrame, text='股票名称', font=ft3)
    RecordPriceLab = Label(RecordFrame, text='股票价格', font=ft3)
    RecordNoteLab = Label(RecordFrame, text='备注', font=ft3)

    # RecordDateEntry = Entry(RecordFrame)
    RecordNameEntry = Entry(RecordFrame, font=(None, 11))
    RecordPriceEntry = Entry(RecordFrame, font=(None, 11))
    RecordNoteEntry = Entry(RecordFrame, font=(None, 11))


    # 记录市价执行程序
    def record():
        try:
            price = float(RecordPriceEntry.get())
        except ValueError:
            showerror('输入不合法', '请输入数字')
            return
        name = RecordNameEntry.get()
        if name == '':
            showerror('缺少名称', '请输入名称')
            return
        confirm = askquestion('记录确认', '{} 现在市价为{}元每股。'.format(name, price))
        if confirm:
            error = User.record_price_today(name, price, RecordNoteEntry.get())
            if error is not None:
                showerror(error, '输入市价或名字不正确')
                return
            update_table()
            update_history()


    RecordButton = Button(RecordFrame, text='记录市价', command=record, font=ft3)

    # 放置交易页面内容
    # BuyDateLab.grid(row=0, column=0, sticky=N)
    # BuyDateEntry.grid(row=0, column=1, sticky=N)
    BuyNameLab.grid(row=0, column=1)
    BuyNameEntry.grid(row=0, column=2)
    BuyPriceLab.grid(row=1, column=1)
    BuyPriceEntry.grid(row=1, column=2)
    BuyNumLab.grid(row=2, column=1)
    BuyNumEntry.grid(row=2, column=2)
    BuyNoteLab.grid(row=3, column=1)
    BuyNoteEntry.grid(row=3, column=2)
    BuyButton.grid(row=4, columnspan=4)
    Frame(BuyFrame, width=220).grid(row=0, column=3, rowspan=3)
    Frame(BuyFrame, width=259).grid(row=0, column=0, rowspan=3)

    # SellDateLab.grid(row=0, column=0)
    # SellDateEntry.grid(row=0, column=1)
    SellNameLab.grid(row=0, column=1)
    SellNameEntry.grid(row=0, column=2)
    SellPriceLab.grid(row=1, column=1)
    SellPriceEntry.grid(row=1, column=2)
    SellNumLab.grid(row=2, column=1)
    SellNumEntry.grid(row=2, column=2)
    SellNoteLab.grid(row=3, column=1)
    SellNoteEntry.grid(row=3, column=2)
    SellButton.grid(row=4, columnspan=4)
    Frame(SellFrame, width=220).grid(row=0, column=3, rowspan=3)
    Frame(SellFrame, width=259).grid(row=0, column=0, rowspan=3)

    # RecordDateLab.grid(row=0, column=0)
    RecordNameLab.grid(row=0, column=1)
    RecordPriceLab.grid(row=1, column=1)
    # RecordDateEntry.grid(row=0, column=1)
    RecordNameEntry.grid(row=0, column=2)
    RecordPriceEntry.grid(row=1, column=2)
    RecordNoteLab.grid(row=2, column=1)
    RecordNoteEntry.grid(row=2, column=2)

    Frame(RecordFrame, height=29).grid(row=3)

    RecordButton.grid(row=4, columnspan=4)

    Frame(RecordFrame, width=220).grid(row=0, column=3, rowspan=3)
    Frame(RecordFrame, width=259).grid(row=0, column=0, rowspan=3)

    # 显示股市表格内容

    stocks_tab = Treeview(TableFrame, columns=HEADING, show='headings',
                          height=37)
    scroll_bar = Scrollbar(TableFrame, orient=VERTICAL,
                           command=stocks_tab.yview, width=10)
    stocks_tab.configure(yscrollcommand=scroll_bar.set)

    for i in range(Stock.INFO_PCS_NUM):
        stocks_tab.column(HEADING[i], width=COL_WID[i], anchor='center')
        stocks_tab.heading(HEADING[i], text=HEADING[i])


    def select_stock(event):

        name = ''
        price = ''

        for item in stocks_tab.selection():
            name = stocks_tab.item(item, 'values')[Stock.NAME]
            price = stocks_tab.item(item, 'values')[Stock.PRICE_TODAY]

        NameList = [BuyNameEntry, RecordNameEntry, SellNameEntry,
                    StockNameEntry, CashNameEntry]
        PriceList = [SellPriceEntry, BuyPriceEntry, RecordPriceEntry]

        for entry in NameList:
            entry.delete(0, END)
            entry.insert(0, name)

        for entry in PriceList:
            entry.delete(0, END)
            entry.insert(0, price)


    stocks_tab.bind('<ButtonRelease-1>', select_stock)


    def update_table():

        TotalMarketPrice = 0

        for item in stocks_tab.get_children():
            stocks_tab.delete(item)

        with open(User.get_stock_file(), 'r', encoding='UTF-8-sig') as f:
            all_stock = csv.reader(f)
            f.readline()
            for line in all_stock:
                if line == []:
                    break
                stocks_tab.insert('', 'end', values=tuple(line))
                TotalMarketPrice += float(line[Stock.MARKET_PRICE])

        depo = convert_float_to_comma_sep_number(User.get_deposit())
        CurrDepositNum = Label(DataFrame, text=depo + ' 元', font=ft1,
                               bg='white', width=20)
        CurrDepositNum.grid(row=0, column=1)

        rev = convert_float_to_comma_sep_number(
            User.get_deposit() + TotalMarketPrice)
        CurrTotalNum = Label(DataFrame, text=rev + ' 元', font=ft1, bg='white',
                             width=20)
        CurrTotalNum.grid(row=1, column=1)

        # 总盈利 Label 操作
        pro_loss = round(
            User.get_deposit() + TotalMarketPrice - User.fund_movement, 2)
        if pro_loss <= 0:
            color = 'forestgreen'
        else:
            color = 'red'
        profit = convert_float_to_comma_sep_number(pro_loss)
        CurrProfitNum = Label(DataFrame, text=profit + ' 元', fg=color, font=ft1,
                              bg='white', width=20)
        CurrProfitNum.grid(row=2, column=1)

        clear_input()


    # 放置表格
    stocks_tab.grid(row=0, column=0, sticky=N)
    scroll_bar.grid(row=0, column=1, sticky=N + S)

    # 显示历史记录

    operation_history = Treeview(HistoryFrame, columns=HISTORY_HEADER,
                                 show='headings')
    scroll_bar = Scrollbar(HistoryFrame, orient=VERTICAL,
                           command=operation_history.yview)
    operation_history.configure(yscrollcommand=scroll_bar.set)

    for i in range(Stock.HISTORY_PCS_NUM):
        operation_history.column(HISTORY_HEADER[i], width=HISTORY_COL_WID[i])
        operation_history.heading(HISTORY_HEADER[i], text=HISTORY_HEADER[i])


    def update_history():

        for item in operation_history.get_children():
            operation_history.delete(item)

        with open(User.get_history_file(), 'r', encoding='UTF-8-sig') as f:
            all_history = csv.reader(f)
            f.readline()
            for line in all_history:
                operation_history.insert('', 'end', values=tuple(line))


    # 放置表格
    operation_history.grid(row=0, column=0, sticky=W)
    scroll_bar.grid(row=0, column=1, sticky=N + S)

    # 存取款页面
    #
    # CurrDepositLab = Label(DepositFrame, text='deposits')
    # CurrDepositLab.grid(row=2, columnspan=2)

    # 存款页面
    # IncomeDateLab = Label(IncomeFrame, text='date')
    IncomeNumLab = Label(IncomeFrame, text='金额', font=ft3)
    IncomeNoteLab = Label(IncomeFrame, text='备注', font=ft3)

    # IncomeDateEntry = Entry(IncomeFrame)
    IncomeNumEntry = Entry(IncomeFrame, font=(None, 11))
    IncomeNoteEntry = Entry(IncomeFrame, font=(None, 11))


    def deposit():
        try:
            amount = float(IncomeNumEntry.get())
        except ValueError:
            showerror('Error', '请输入数字存款')
            return
        amount_str = convert_float_to_comma_sep_number(amount)
        remain_str = convert_float_to_comma_sep_number(
            User.get_deposit() + amount)
        confirm = askokcancel('存款确认',
                              '存入{}元，操作后总存款为{}元'.format(amount_str, remain_str))
        if confirm:
            error = User.income(amount, IncomeNoteEntry.get())
            if error is not None:
                showerror(error, '无法处理负数输入')
                return
            update_table()
            update_history()


    IncomeButton = Button(IncomeFrame, text='存款', command=deposit, font=ft3)

    # 取款页面
    # ExpenseDateLab = Label(ExpenseFrame, text='date')
    ExpenseNumLab = Label(ExpenseFrame, text='金额', font=ft3)
    ExpenseNoteLab = Label(ExpenseFrame, text='备注', font=ft3)

    # ExpenseDateEntry = Entry(ExpenseFrame)
    ExpenseNumEntry = Entry(ExpenseFrame, font=(None, 11))
    ExpenseNoteEntry = Entry(ExpenseFrame, font=(None, 11))


    def expend():
        try:
            amount = float(ExpenseNumEntry.get())
        except ValueError:
            showerror('Error', '请输入数字存款')
            return
        if amount > User.get_deposit():
            showerror('余款不足', '余款不足')
            return
        amount_str = convert_float_to_comma_sep_number(amount)
        remain_str = convert_float_to_comma_sep_number(
            User.get_deposit() - amount)
        confirm = askokcancel('存款确认',
                              '取款{}元，操作后总存款为{}元'.format(amount_str, remain_str))
        if confirm:
            error = User.expense(amount, ExpenseNoteEntry.get())
            if error is not None:
                showerror(error, '无法处理负数输入')
                return
            update_table()
            update_history()


    ExpenseButton = Button(ExpenseFrame, text='取款', command=expend, font=ft3)

    DepositAmountLab = Label(DepositFrame, text='Deposit')

    # IncomeDateLab.grid(row=0, column=0)
    # IncomeDateEntry.grid(row=0, column=1)
    Frame(IncomeFrame, height=12).grid(row=1)
    IncomeNumLab.grid(row=0, column=1)
    IncomeNumEntry.grid(row=0, column=2)
    Frame(IncomeFrame, height=44).grid(row=3)
    IncomeNoteLab.grid(row=2, column=1)
    IncomeNoteEntry.grid(row=2, column=2)
    IncomeButton.grid(row=4, columnspan=4)
    Frame(IncomeFrame, width=260).grid(row=0, column=3, rowspan=3)
    Frame(IncomeFrame, width=260).grid(row=0, column=0, rowspan=3)

    # ExpenseDateLab.grid(row=0, column=0)
    # ExpenseDateEntry.grid(row=0, column=1)
    Frame(ExpenseFrame, height=12).grid(row=1)
    ExpenseNumLab.grid(row=0, column=1)
    ExpenseNumEntry.grid(row=0, column=2)
    ExpenseNoteLab.grid(row=2, column=1)
    ExpenseNoteEntry.grid(row=2, column=2)
    Frame(ExpenseFrame, height=44).grid(row=3)
    ExpenseButton.grid(row=4, columnspan=4)
    Frame(ExpenseFrame, width=260).grid(row=0, column=3, rowspan=3)
    Frame(ExpenseFrame, width=260).grid(row=0, column=0, rowspan=3)

    # 分红页面

    # 分红利
    # CashDateLab = Label(CashShareFrame, text='date')
    CashNameLab = Label(CashShareFrame, text='股票名称', font=ft3)
    CashRateLab = Label(CashShareFrame, text='每股股息（元）', font=ft3)
    CashNoteLab = Label(CashShareFrame, text='备注', font=ft3)

    # CashDateEntry = Entry(CashShareFrame)
    CashNameEntry = Entry(CashShareFrame, font=(None, 11))
    CashRateEntry = Entry(CashShareFrame, font=(None, 11))
    CashNoteEntry = Entry(CashShareFrame, font=(None, 11))


    def share_cash():
        try:
            name = CashNameEntry.get()
            rate = float(CashRateEntry.get())
        except ValueError:
            showerror('Error', '请输入数字')
            return
        confirm = askokcancel('分红确认', '您即将从{} 获得每股红利{} 元'.format(name, rate))
        if confirm:
            error = User.give_share(name, rate, CashNoteEntry.get())
            if error is not None:
                showerror(error, '请输入正确的名称和利率')
                return
            update_table()
            update_history()


    CashButton = Button(CashShareFrame, text='分股息', command=share_cash,
                        font=ft3)

    # 分红股
    # StockDateLab = Label(StockShareFrame, text='date')
    StockNameLab = Label(StockShareFrame, text='股票名称', font=ft3)
    StockRateLab = Label(StockShareFrame, text='每股分红（股）', font=ft3)
    StockNoteLab = Label(StockShareFrame, text='备注', font=ft3)

    # StockDateEntry = Entry(StockShareFrame)
    StockNameEntry = Entry(StockShareFrame, font=(None, 11))
    StockRateEntry = Entry(StockShareFrame, font=(None, 11))
    StockNoteEntry = Entry(StockShareFrame, font=(None, 11))


    def stock_cash():
        try:
            name = StockNameEntry.get()
            rate = float(StockRateEntry.get())
        except ValueError:
            showerror('Error', '请输入数字')
            return
        confirm = askokcancel('分红确认', '您即将从{} 每股额外获得{} 股'.format(name, rate))
        if confirm:
            error = User.give_share(name, rate, StockNoteEntry.get(),
                                    cash_share=False)
            if error is not None:
                showerror(error, '请输入正确的名称和利率')
                return
            update_table()
            update_history()


    StockButton = Button(StockShareFrame, text='分红股', command=stock_cash,
                         font=ft3)

    # StockDateLab.grid(row=0)
    StockNameLab.grid(row=0, column=1)
    StockRateLab.grid(row=1, column=1)
    StockNoteLab.grid(row=2, column=1)

    # StockDateEntry.grid(row=0, column=1)
    StockNameEntry.grid(row=0, column=2)
    StockRateEntry.grid(row=1, column=2)
    StockNoteEntry.grid(row=2, column=2)

    # CashDateLab.grid(row=0)
    CashNameLab.grid(row=0, column=1)
    CashRateLab.grid(row=1, column=1)
    CashNoteLab.grid(row=2, column=1)

    # CashDateEntry.grid(row=0, column=1)
    CashNameEntry.grid(row=0, column=2)
    CashRateEntry.grid(row=1, column=2)
    CashNoteEntry.grid(row=2, column=2)

    Frame(StockShareFrame, height=28).grid(row=3)
    Frame(CashShareFrame, height=28).grid(row=3)

    CashButton.grid(row=4, columnspan=4)
    StockButton.grid(row=4, columnspan=4)

    Frame(CashShareFrame, width=210).grid(row=0, column=3, rowspan=3)
    Frame(StockShareFrame, width=210).grid(row=0, column=0, rowspan=3)
    Frame(CashShareFrame, width=210).grid(row=0, column=0, rowspan=3)
    Frame(StockShareFrame, width=210).grid(row=0, column=3, rowspan=3)

    ALL_ENTRY = [ExpenseNumEntry,
                 ExpenseNoteEntry,
                 IncomeNumEntry,
                 IncomeNoteEntry,
                 BuyPriceEntry,
                 BuyNumEntry,
                 BuyNameEntry,
                 BuyNoteEntry,
                 RecordNoteEntry,
                 RecordNameEntry,
                 RecordPriceEntry,
                 SellPriceEntry,
                 SellNumEntry,
                 SellNameEntry,
                 SellNoteEntry,
                 StockNoteEntry,
                 StockNameEntry,
                 StockRateEntry,
                 CashNoteEntry,
                 CashNameEntry,
                 CashRateEntry

                 ]


    def clear_input():

        for entry in ALL_ENTRY:
            entry.delete(0, END)


    # 数据页面

    DepositLab = Label(DataFrame, text='  资金余额: ', font=ft2)
    TotalLab = Label(DataFrame, text='     总资产: ', font=ft2)
    RevenueLab = Label(DataFrame, text='         盈亏: ', font=ft2)

    DepositLab.grid(row=0, column=0, sticky=W)
    TotalLab.grid(row=1, column=0, sticky=W)
    RevenueLab.grid(row=2, column=0, sticky=W)

    # 菜单栏

    menubar = Menu(root)

    about = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='关于', menu=about)


    def instruction():
        instruct = Toplevel()
        instruct.title('')

        struct = Frame(instruct, height=600, width=400)
        Frame(struct, height=10, width=400).grid(row=0)
        # Label(ip, image=Logo1).grid(row=1)
        Label(struct, text='计算公式', font=('Times', 11)).grid(row=2)
        Label(struct,
              text='成本价（买入）= [原成本价 * 现持股数 +（交易价 + 费率）* 买入股数] / （现持股数 + 买入股数） ',
              font=('Times', 11)).grid(row=3)
        Label(struct,
              text='成本价（卖出）= [原成本价 * 现持股数 -（交易价 + 费率）* 卖出股数] / （现持股数 - 卖出股数） ',
              font=('Times', 11)).grid(row=4)
        Label(struct, text='市值 = 市价 * 持股数 ', font=('Times', 11)).grid(row=5)
        Label(struct, text='浮动盈亏 =（市价 - 成本价）* 现持股数',
              font=('Times', 11)).grid(row=6)
        Label(struct, text='历史盈亏 = 浮动盈亏历史累计',
              font=('Times', 11)).grid(row=7)
        Label(struct, text='总资产 = 资金余额 + 所有股票市值',
              font=('Times', 11)).grid(row=8)
        Label(struct, text='盈亏 = 总资产 - 存取款历史总计',
              font=('Times', 11)).grid(row=9)
        struct.pack()


    def credentials():
        credit = Toplevel()
        credit.title('')

        ip = Frame(credit, height=300)
        Frame(ip, height=10, width=400).grid(row=0)
        # Label(ip, image=Logo1).grid(row=1)
        Label(ip, text='CUi 股票管理系统', font=('Times', 11)).grid(row=2)
        Label(ip, text='制作者：崔泊远', font=('Times', 11)).grid(row=3)
        Label(ip, text='ver.1.3.2.190819-beta', font=('Courier', 11)).grid(
            row=4)

        ip.pack()


    about.add_command(label='使用说明', font=('Times', 11), command=instruction)
    about.add_command(label='Credentials', font=('Times', 11),
                      command=credentials)

    settings = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='设置', menu=settings, font=('Times', 11))


    def clear_all():

        confirm = askokcancel('确认清除所有数据？', '确认清除包括所有股票记录、操作历史记录、以及资产记录的数据？')
        if confirm:
            User.clear_all()
            update_table()
            update_history()
        else:
            return


    def edit_service_fee():

        win1 = Toplevel()
        win1.title('更改费率')

        OldLab = Label(win1, text='原始费率:')
        OldVal = Label(win1, text=str(User.get_service_fee_rate()))
        NewLab = Label(win1, text='新费率:')
        NewVal = Entry(win1)

        def change_fee_rate():
            try:
                new_rate = float(NewVal.get())
            except ValueError:
                showerror('非法输入', '请输入数字')
                return
            User.edit_service_fee_rate(new_rate)
            win1.destroy()
            showinfo('确认', '更改成功')

        okButton = Button(win1, text='确定', command=change_fee_rate)

        OldLab.grid(row=0, column=0)
        OldVal.grid(row=0, column=1)
        NewLab.grid(row=1, column=0)
        NewVal.grid(row=1, column=1)
        okButton.grid(row=2, columnspan=2)


    def switch():
        account_win(toplevel=True)
        root.quit()
        root.destroy()


    switch_button = Button(TitleFrame2, text='切换', command=switch, bg='white',
                           bd=1, relief='groove', font=('Verdana', 10))
    switch_button.grid(row=0, column=1, padx=(5, 0), pady=(2, 0))


    def check_note():
        user_note = Toplevel()
        notes = Text(user_note)
        which_user = Label(user_note, text='{} 的账户备注'.format(User.name))

        def save():
            new_notes = notes.get('1.0', END)
            new_accounts = []
            new_user = []
            for _ in range(5):
                new_user.append('NA')
            with open(ACCOUNTS, 'r', encoding='UTF-8-sig') as o:
                accounts_read = csv.reader(o)
                for line in accounts_read:
                    if line == []:
                        continue
                    if line[0] == User.name:
                        new_user[0] = User.name
                        new_user[1] = new_notes
                        new_user[2] = User.get_stock_file()
                        new_user[3] = User.get_history_file()
                        new_user[4] = User.get_asset_record()
                        new_accounts.append(new_user)
                        continue
                    new_accounts.append(line)
            with open(ACCOUNTS, 'w', encoding='UTF-8-sig', newline='') as w:
                accounts_write = csv.writer(w)
                for line in new_accounts:
                    accounts_write.writerow(line)
                    # print(line)

            showinfo('更改备注', '成功更改备注。')

        save_button = Button(user_note, text='保存备注', command=save)
        notes.insert(END, Account['note'])

        notes.grid(row=1, pady=(10, 10), padx=(10, 10))
        which_user.grid(row=0, pady=(10, 10), padx=(10, 10))
        save_button.grid(row=2, pady=(10, 10))


    settings.add_command(label='设置费率', command=edit_service_fee,
                         font=('Times', 11))
    # settings.add_command(label='切换账户', command=switch, font=('Times', 11))
    settings.add_command(label='此账户备注', command=check_note, font=('Times', 11))
    settings.add_separator()
    settings.add_command(label='清除所有', command=clear_all, font=('Times', 11))

    update_table()
    update_history()

    root.config(menu=menubar)
    root.mainloop()

print('耶')
