# -*- coding: UTF-8 -*-
from tkinter import *
from tkinter import ttk
import tkinter.ttk
import tkinter.messagebox
import tkinter.font as tkFont
# import ctypes
from datetime import datetime
import requests
import base64
import os

# pip install pywin32

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
	"Content-Type": "application/x-www-form-urlencoded",
	"X-Forwarded-For": "127.0.0.1",
}


def get_time(_):
	year = datetime.now().year
	month = datetime.now().month
	if _ == 1: year -= 1
	if _ == 2: year = 1999; month = 1
	if len(str(month)) == 1: month = "0" + str(month)
	return year, month


def send_req(_, txt_api, txt_search, cb_time, cb_is_web, txt_res, cb_save, save_name, status_code):
	if len(txt_api) < 1:
		tkinter.messagebox.showinfo('\u5e2e\u52a9', '\u4ee4\u724c\u4e3a\u7a7a')
		return

	if cb_save.get() == 1 and save_name == "":
		tkinter.messagebox.showinfo('\u5e2e\u52a9', '\u4fdd\u5b58\u6587\u4ef6\u540d\u4e3a\u7a7a')
		return

	if _ == 1:	# or _ == 2
		r = requests.get(f'https://hunter.qianxin.com/openApi/search/batch/999999999?api-key={txt_api}', headers=headers)
		if '401' in r.text:
			tkinter.messagebox.showinfo('\u5e2e\u52a9', '\u4ee4\u724c\u8fc7\u671f')
		elif '400' in r.text:
			tkinter.messagebox.showinfo('\u5e2e\u52a9', '\u9a8c\u8bc1\u901a\u8fc7')

	if _ == 2:
		_ = get_time(cb_time)
		bs64_search = base64.urlsafe_b64encode(txt_search.encode("utf-8")).decode("utf-8")
		url = 'https://hunter.qianxin.com/openApi/search/batch?api-key={}&search={}&status_code={}&is_web={}&start_time="{}-{}-01 00:00:00"&end_time="9999-01-01 00:00:00"'.format(
			txt_api, bs64_search, status_code, cb_is_web, _[0], _[1])
		r = requests.post(url, headers=headers)
		res = r.json()

		txt_res.config(state=NORMAL)
		if res['code'] == 200 and res['data']['filename'] != '':

			while True:
				url = 'https://hunter.qianxin.com/openApi/search/batch/{}?api-key={}'.format(res['data']['task_id'], txt_api)
				r = requests.get(url, headers=headers)
				export_process = r.json()
				txt_res.insert(INSERT, export_process['data']['status'] + ": " + export_process['data']['progress'] + "\n")
				if export_process['data']['progress'] == '100%': break
				import time; time.sleep(1)

			task_id = res['data']['task_id']
			if cb_save.get() == 1 and save_name != "":
				cmd = 'curl -X GET -k "https://hunter.qianxin.com/openApi/search/download/{}?api-key={}" -o {}.csv'.format(
					task_id, txt_api, save_name)
				print('\n' + cmd + '\n')
				os.system(cmd)
				tkinter.messagebox.showinfo('\u5e2e\u52a9', '\u5df2\u4fdd\u5b58\u005b\u6ce8\u610f\u8986\u76d6\u005d')

			txt_res.insert(INSERT, "https://hunter.qianxin.com/openApi/search/download/{}?api-key={}".format(task_id, txt_api) + "\n")
			txt_res.insert(INSERT, res['data']['consume_quota'] + "\n")
			txt_res.insert(INSERT, res['data']['rest_quota'] + "\n\n")
		elif res['code'] == 200 and res['data']['filename'] == '':
			tkinter.messagebox.showinfo('\u5e2e\u52a9', res['data']['state'])
			txt_res.insert(INSERT, 'https://hunter.qianxin.com/openApi/search/download/{}?api-key={}'.format(res['data']['task_id'], txt_api) + "\n\n")

			if cb_save.get() == 1 and save_name != "":
				cmd = 'curl -X GET -k "https://hunter.qianxin.com/openApi/search/download/{}?api-key={}" -o {}.csv'.format(
					res['data']['task_id'], txt_api, save_name)
				print('\n' + cmd + '\n')
				os.system(cmd)
				tkinter.messagebox.showinfo('\u5e2e\u52a9', '\u5df2\u4fdd\u5b58\u005b\u6ce8\u610f\u8986\u76d6\u005d')
		else:
			tkinter.messagebox.showinfo('\u5e2e\u52a9', res['message'])
		
		txt_res.config(state=DISABLED)


def show_txt(cb_save, txt_save):
	txt_save.place(x=width//5*4-20, y=140, width=width//5, height=screenHeight // 40) if cb_save.get() == 1 else txt_save.place_forget()


def status_bar():
	status = StringVar()
	status.set(datetime.now().strftime("%Y年%m月%d日 %H:%M:%S") + '\t © \u0062\u0079\u0020\u0030\u0039')
	Label(root, textvariable=status, bg='white', anchor="w").place(x=0, y=height-height//20, width=width, height=screenHeight//45)
	root.after(1000, status_bar)


def init():
	menubar = Menu(root)
	menu_info_search = Menu(menubar, tearoff=0)
	menubar.add_cascade(label='\u5e2e\u52a9', menu=menu_info_search)

	submenu = Menu(menu_info_search, tearoff=0)
	menu_info_search.add_cascade(label='\u67e5\u8be2\u8bed\u6cd5', menu=submenu)
	menu_info_search.add_cascade(label='\u72b6\u6001\u7801\u5217\u8868\uff0c\u4ee5\u9017\u53f7\u5206\u9694\uff0c\u5982\u201d\u0032\u0030\u0030\u002c\u0034\u0030\u0031\u201c')
	submenu.add_command(label='搜索技巧', command=lambda: tkinter.messagebox.showinfo('\u5e2e\u52a9', '\u7cbe\u786e\u67e5\u8be2\u53ef\u4ee5\u4f7f\u7528\u201c\u003d\u003d\u201d\uff1b\u0020\u6a21\u7cca\u67e5\u8be2\u53ef\u4ee5\u4f7f\u7528\u201c\u003d\u201d\uff1b\u7cbe\u786e\u5254\u9664\u53ef\u4ee5\u4f7f\u7528\u201c\u0021\u003d\u003d\u201d\uff1b\u0020\u6a21\u7cca\u5254\u9664\u53ef\u4ee5\u4f7f\u7528\u201c\u0021\u003d\u201d\uff1b\u0020\u53ef\u4ee5\u4f7f\u7528\u0020\u0061\u006e\u0064\u3001\u0020\u0026\u0026\u6216\u0020\u006f\u0072\u3001\u0020\u007c\u007c\u0020\u8fdb\u884c\u591a\u79cd\u6761\u4ef6\u7ec4\u5408\u67e5\u8be2'))

	root.config(menu=menubar)

	lbl_w, txt_w, btn_w = 100, 100, 100
	Label(root, text='API-KEY', bg='white').place(x=20, y=20, width=lbl_w, height=screenHeight//40)
	Label(root, text='查询条件', bg='white').place(x=20, y=80, width=lbl_w, height=screenHeight//40)
	txt_api = Text(root, wrap='none', bg='black', fg='yellow'); txt_api.place(x=140, y=20, width=width-200-btn_w, height=screenHeight//40); txt_api.insert("insert", api_key)
	txt_search = Text(root, wrap='none', bg='black', fg='yellow'); txt_search.place(x=140, y=80, width=width-200-btn_w, height=screenHeight//40)

	Button(root, text='验证', command=lambda: send_req(1, txt_api.get('0.0', 'end').split('\n')[0], txt_search.get('0.0', 'end').split('\n')[0], cb_time.current(), cb_is_web.current()+1, txt_res, cb_save, txt_save.get('0.0', 'end').split('\n')[0], txt_status_code.get('0.0', 'end').split('\n')[0])).place(x=width-40-btn_w, y=20, width=btn_w, height=screenHeight//40)
	Button(root, text='查询', command=lambda: send_req(2, txt_api.get('0.0', 'end').split('\n')[0], txt_search.get('0.0', 'end').split('\n')[0], cb_time.current(), cb_is_web.current()+1, txt_res, cb_save, txt_save.get('0.0', 'end').split('\n')[0], txt_status_code.get('0.0', 'end').split('\n')[0])).place(x=width-40-btn_w, y=80, width=btn_w, height=screenHeight//40)

	Label(root, text='状态码', bg='white').place(x=20, y=140, width=lbl_w, height=screenHeight//40)
	txt_status_code = Text(root, wrap='none', bg='black', fg='yellow'); txt_status_code.place(x=140, y=140, width=width-200-btn_w-lbl_w, height=screenHeight//40)
	txt_status_code.insert(INSERT, "200,401,403,404")

	cb_time = ttk.Combobox(
		master=root,
		state="readonly",
		cursor="arrow",
		values=['\u672c\u6708', '\u6700\u8fd1\u0031\u5e74', '\u0031\u0039\u0039\u0039\u002d\u0039\u0039\u0039\u0039\u005b\u614e\u7528\u005d'],
	)
	cb_time.current(0)
	cb_time.place(x=20, y=200, width=width//5+20, height=screenHeight//40)

	cb_is_web = ttk.Combobox(
		master=root,
		state="readonly",
		cursor="arrow",
		values=['\u0077\u0065\u0062\u670d\u52a1\u8d44\u4ea7', '非\u0077\u0065\u0062\u670d\u52a1\u8d44\u4ea7', '\u5168\u90e8'],
	)
	cb_is_web.current(0)
	cb_is_web.place(x=width//5+60, y=200, width=width//5+20, height=screenHeight // 40)

	cb_save = IntVar()
	Checkbutton(root, text='保存', variable=cb_save, onvalue=1, offvalue=0, bg="white", command=lambda: show_txt(cb_save, txt_save)).place(x=width-width//5-20-lbl_w, y=140, width=lbl_w, height=screenHeight // 40)
	txt_save = Text(root, wrap='none', bg='WhiteSmoke', padx=5, pady=5, font=tkFont.Font(weight=tkFont.BOLD))

	txt_res = Text(root, wrap='word', font=tkFont.Font(weight=tkFont.BOLD), bg='WhiteSmoke')
	txt_res.place(x=0, y=260, width=width-width//25+5, height=height-260-screenHeight//45)

	scroll_res = Scrollbar(); scroll_res.place(x=width-width//25, y=260, width=width//25, height=height-260-screenHeight//45)
	scroll_res.config(command=txt_res.yview); txt_res.config(yscrollcommand=scroll_res.set)
	txt_res.config(state=DISABLED)

	status_bar()


if __name__ == '__main__':
	api_key = ''

	root = Tk()
	root.title('\u0048\u0075\u006e\u0074\u0065\u0072\u0020\u0047\u0072\u0061\u0070\u0068\u0069\u0063\u0061\u006c')
	root.configure(bg='white')

	ctypes.windll.shcore.SetProcessDpiAwareness(1)
	ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
	root.tk.call('tk', 'scaling', ScaleFactor / 75)

	screenWidth, screenHeight = 2160, 1440
	width = screenWidth // 5 * 3 if screenWidth < screenHeight else screenHeight // 5 * 3
	height = width // 5 * 4
	root.geometry("{}x{}+{}+{}".format(width, height, screenWidth // 2 - width // 2, screenHeight // 2 - height // 2))
	root.minsize(width, height)
	root.maxsize(width, height)

	init()

	root.mainloop()
