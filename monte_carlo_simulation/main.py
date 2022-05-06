from tkinter import *
from tkinter import messagebox
import calculator
import chart_plotter
import monte_carlo
from calculator import Calculator
from chart_plotter import ChartPlotter
import matplotlib.pyplot as plt
from tkinter.filedialog import askdirectory
from datetime import datetime
import time
import os

class MyStockApp:
    def __init__(self):
        self.root = Tk()
        # self.root.geometry('800x800')
        self.root.title('MonteFolio')
        for i in range(9):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        # Row_0
        intro_text = '欢迎来到MonteFolio! \n请输入一系列股票代码进行进一步分析\n(参照stooq数据库的Ticker格式)'
        self.intro = Label(self.root, text=intro_text, font=(10,),foreground='blue', underline=1, anchor='nw',pady=5,justify=CENTER)
        self.intro.grid(row=0,columnspan=4,column=0,sticky=N)
        # Row_1
        self.days_back_label = Label(self.root, text='时间期限：',anchor='e')
        self.days_back_label.grid(row=1,column=0,sticky=E)
        self.days_back = Entry(self.root, width=8)
        self.days_back.grid(row=1,column=1,sticky=W)
        self.mc_sims_label = Label(self.root, text='模拟次数：')
        self.mc_sims_label.grid(row=1, column=2,sticky=E)
        self.mc_sims = Entry(self.root, width=8)
        self.mc_sims.grid(row=1, column=3,sticky=W)
        # Row_2
        self.stock_entry_label = Label(self.root, text='股票代码：')
        self.stock_entry_label.grid(row=2,column=0,sticky=E)
        self.stock_entry = Entry(self.root, width=8)
        self.stock_entry.grid(row=2,column=1,sticky=W)
        self.stock_entry.bind('<Return>', self.add_stock)
        self.initial_portfolio_label = Label(self.root, text='初始资本：')
        self.initial_portfolio_label.grid(row=2, column=2, sticky=E)
        self.initial_portfolio = Entry(self.root, width=8)
        self.initial_portfolio.grid(row=2, column=3, sticky=W)
        # Row_3
        self.var1 = IntVar()
        self.save_pic_label = Checkbutton(self.root, text='保存输出',variable=self.var1,command=self.save_pic,onvalue=1,offvalue=0)
        self.save_pic_label.grid(row=3, column=0, rowspan=1)
        self.query_btn = Button(self.root, text='查询', command=self.new_query)
        self.query_btn.grid(row=3, column=1)
        self.entry_frame = Frame(self.root)
        self.add_button = Button(self.entry_frame, text='添加股票', command=self.add_stock)
        self.delete_button = Button(self.entry_frame, text='删除股票', command=self.delete_stock)
        self.entry_frame.grid(row=3, column=2, columnspan=2,sticky=W)
        self.add_button.pack(side=LEFT)
        self.delete_button.pack(side=LEFT)
        # Row_4
        self.choice_frame = Frame(self.root)
        self.plot_price_button = Button(self.choice_frame, text='历史行情', command=self.plot_price)
        self.plot_returns_button = Button(self.choice_frame, text='收益率', command=self.plot_returns)
        self.monte_carlo_button = Button(self.choice_frame, text='蒙特卡洛', command=self.monte_carlo)
        self.monte_carlo_old_button = Button(self.choice_frame, text='收益情况', command=self.monte_carlo_old)
        self.choice_frame.grid(row=4, column=0, columnspan=4)
        self.plot_price_button.pack(side=LEFT)
        self.plot_returns_button.pack(side=LEFT)
        self.monte_carlo_button.pack(side=LEFT)
        self.monte_carlo_old_button.pack(side=LEFT)
        # Sub-screen
        self.window = Toplevel()
        self.window.title('')
        self.selected_stock_list_label = Label(self.window, text='已选股票')
        self.selected_stock_list_label.pack()
        self.selected_stock_list = Listbox(self.window,border=0,width=12,selectmode=SINGLE)
        self.selected_stock_list.configure(justify=CENTER)
        self.selected_stock_list.pack()
        # Row_5
        self.output_directory_label = Label(self.root,text='输出路径：')
        self.output_directory_label.grid(row=5,column=0,sticky=E)
        self.output_directory = Entry(self.root, width=20,state='disabled')
        self.output_directory.grid(row=5, column=1, sticky=W,columnspan=2)
        self.output_directory_select = Button(text='选择路径',command=self.selectPath,state='disabled')
        self.output_directory_select.grid(row=5,column=3)
        # Row_6
        self.log_label = Label(self.root, text='系统日志：')
        self.log_label.grid(row=6)
        self.log = Text(self.root,width=50,height=10,highlightthickness=0)
        self.log.grid(row=7,column=0,columnspan=4,padx=10,pady=5,sticky=N)

        # self.system_info_label = Label(self.root, text='系统消息')
        # self.system_info_label.grid(row=6,column=1,sticky=N+W)
        # self.system_info = Text(self.root)
        # self.system_info.grid(row=6,column=1,columnspan=1,rowspan=1,sticky=N+W)


        #
        # self.selected_stock_list = Listbox(self.root, width=8, border=0, selectmode=SINGLE,)
        # self.selected_stock_list.configure(justify=CENTER)
        # self.selected_stock_list.grid(row=3, column=5, rowspan=4, pady=5,padx=5)

        # self.tfield = Text(self.root)
        # self.tfield.grid(row=0,column=5,rowspan=9,padx=5)


        self.logger('Hello World! ')
        self.validation = False
        self.save_fig = False
        self.auto_fillin()
        self.root.mainloop()

    def now(self):
        return datetime.now().strftime('%H:%M:%S')

    def selectPath(self):
        path_ = askdirectory()
        if path_ == '':
            self.logger('路径不能为空！')
        else:
            self.output_directory.delete(0,END)
            self.output_directory.insert(0,path_)
            self.directory = path_
            self.logger(f'已设置输出路径为: {path_}')


    def save_pic(self):
        if self.var1.get() == 0:
            self.output_directory.configure(state='disabled')
            self.output_directory_select.configure(state='disabled')
            self.save_fig = False
        else:
            self.output_directory.configure(state='normal')
            self.output_directory_select.configure(state='normal')
            self.save_fig = True


    def auto_fillin(self):
        self.mc_sims.insert(END, '1000')
        self.days_back.insert(END, '300')
        self.initial_portfolio.insert(END, '10000')

    def new_query(self):
        stockList = list(self.selected_stock_list.get(0,END))
        mc_sims = int(self.mc_sims.get())
        T = int(self.days_back.get())
        initial_portfolio = int(self.initial_portfolio.get())
        days_back = int(int(self.days_back.get()))

        if len(stockList) == 0:
            self.logger(f"股票列表不能为空！")
            return 0
        msg = f"已选择{stockList}，共{len(stockList)}只股票，正在查询..."
        self.logger(msg)
        self.m = monte_carlo.MonteCarloEstimator(stockList, mc_sims, T, initial_portfolio, days_back)

        try:
            self.data = self.m.new_get_data()
            self.logger(f"已查询到数据，可进一步分析！")
            self.validation = True
        except Exception as e:
            self.logger(f"初始化模型失败！请检查参数及网络。")
            print(e)
            return 0
        self.returns = Calculator.get_returns(self.data)
        self.expected_returns = Calculator.get_expectedreturns(self.returns)
        self.covariance = Calculator.get_covariance(self.returns)
        self.cp = ChartPlotter()


    def add_stock(self, *args):
        stock = self.stock_entry.get().upper()
        if_exist = stock in self.selected_stock_list.get(0,END)
        if if_exist:
            self.logger(f'{stock}已存在，请勿重复输入！')
        elif stock == '':
            self.logger(f"股票代码不能为空！")
        else:
            self.selected_stock_list.insert(0, stock)
            self.stock_entry.delete(0, END)
            self.logger(f"添加股票{stock}")

    def delete_stock(self):
        self.selected_stock_list.delete('active')

    def plot_price(self):
        if self.validation:
            ax = self.cp.plot_prices(self.data)
            self.logger(f'已输出近{self.days_back.get()}天的股价趋势图')
            if self.save_fig:
                fname = os.path.join(self.directory, 'stock_prices.png')
                ax.get_figure().savefig(fname, dpi=300)
                self.logger(f"已保存stock_prices.png至指定路径")
        else:
            self.logger('参数不全或尚未查询！')

    def logger(self,msg):
        self.log.insert(END, f"[{self.now()}]"+ msg + '\n')

    def plot_returns(self):
        if self.validation:
            ax = self.cp.plot_returns(self.returns)
            self.logger(f'已输出近{self.days_back.get()}天的收益率')
            if self.save_fig:
                fname = os.path.join(self.directory, 'stock_returns.png')
                ax.get_figure().savefig(fname, dpi=300)
                self.logger(f"已保存stock_returns.png至指定路径")
        else:
            self.logger('参数不全或尚未查询！')

    def monte_carlo(self):
        if self.validation:
            if len(self.m.stockList) < 3:
                self.logger('股票数小于3只，预测情况可能不佳。')
            self.portfolios_allocations_df = self.m.generate_portfolios(self.expected_returns, self.covariance, 0)
            self.portfolio_risk_return_ratio_df = Calculator.map_to_risk_return_ratios(self.portfolios_allocations_df)
            fig = self.cp.plot_portfolios(self.portfolio_risk_return_ratio_df)
            plt.show()
            self.logger(f'已输出Monte Carlo不同投资组合的收益-风险图')
            if self.save_fig:
                fname = os.path.join(self.directory, 'monte_carlo_portfolios.png')
                fig.savefig(fname, dpi=300)
                self.logger(f"已保存monte_carlo_portfolios.png至指定路径")
        else:
            self.logger('参数不全或尚未查询！')

    def monte_carlo_old(self):
        if self.validation:
            self.m.get_data()
            self.m.simulate()
            fig = self.m.plot_simulation()
            self.logger(f'已输出Monte Carlo不同投资组合的未来价值')
            if self.save_fig:
                fname = os.path.join(self.directory, 'monte_carlo_returns.png')
                fig.savefig(fname, dpi=300)
                self.logger(f"已保存monte_carlo_returns.png至指定路径")
        else:
            self.logger('参数不全或尚未查询！')


if __name__ == '__main__':
    MyStockApp()