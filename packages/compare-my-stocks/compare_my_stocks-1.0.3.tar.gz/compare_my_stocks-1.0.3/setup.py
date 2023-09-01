# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['compare_my_stocks',
 'compare_my_stocks.common',
 'compare_my_stocks.config',
 'compare_my_stocks.engine',
 'compare_my_stocks.graph',
 'compare_my_stocks.gui',
 'compare_my_stocks.ib',
 'compare_my_stocks.input',
 'compare_my_stocks.jupyter',
 'compare_my_stocks.processing',
 'compare_my_stocks.resources',
 'compare_my_stocks.tests',
 'compare_my_stocks.transactions']

package_data = \
{'': ['*'],
 'compare_my_stocks': ['.jedi/*',
                       'data/*',
                       'data/jupyter/*',
                       'data/jupyter/.ipynb_checkpoints/*',
                       'ttt/*']}

install_requires = \
['dacite>=1.8.1,<2.0.0']

extras_require = \
{':extra == "full" or extra == "mini" or extra == "jupyter"': ['colorlog>=6.7.0,<6.8.0',
                                                               'django>=3.2.9,<3.2.10',
                                                               'numpy>=1.22.0,<1.23.0',
                                                               'ruamel.yaml>=0.17.31,<0.18.0'],
 'full': ['requests>=2.28.0',
          'pyside6>=6.2.0,<6.3.0',
          'matplotlib==3.5.0rc1',
          'pandas==1.3.2',
          'pytz>=2021.3,<2022.0',
          'qtvoila==2.1.0',
          'superqt>=0.2.5.post1,<0.3.0',
          'mplcursors>=0.4,<1.0',
          'ib-insync>=0.9.85,<0.10.0',
          'pyro5>=5.14,<6.0',
          'ibflex>=0.15,<1.0',
          'six>=1.16.0,<1.17.0',
          'psutil>=5.8.0,<5.9.0',
          'dataconf>=2.1.3,<2.1.4',
          'toml>=0.10.2,<0.11.0',
          'pytest>=7.3.0,<8.0.0',
          'ipykernel',
          'setuptools>=60.2.0,<60.3.0',
          'nbformat>=5.7.3,<5.8.0',
          'json-editor-pyside6>=1.0.3,<2.0.0',
          'qt-collapsible-section-pyside6>=0.1.0,<0.2.0'],
 'jupyter': ['ipykernel', 'voila']}

setup_kwargs = {
    'name': 'compare-my-stocks',
    'version': '1.0.3',
    'description': 'A system for visualizing interesting stocks. Has powerful comparison capabilities and works seamlessly with your jupyter notebook.   Written in QT with matplotlib.',
    'long_description': '\n# Compare My Stocks\n\n## General \nVisualize the performance of stocks in your portfolio or that  you are interested in.\nThere is maximal control over charts, and a variaty of comparision options. \n\nYou can divide the stocks into sectors, and compare the performance of different sector! \n\nFor instance: \n\n* **Chart of profit of sectors in your portfolio and of the entire portfolio relative to a certain point in time.** \n\n![image](https://user-images.githubusercontent.com/72234965/147883101-d565a1b1-eb57-4877-9a2c-706d63b48076.png)\n\n(You won\'t see your portfolio unless you will upload your transactions)  \n\n* **Chart of specific airlines and the airlines as a group compared with nasdaq:**\n \n![image](https://user-images.githubusercontent.com/72234965/149631950-742d1a08-06f7-43ba-a1a3-fa7785f84edf.png)\n\n\n(The difference in the change percentage-wise since 04/01/2021 between ESYJY and the nasdaq is ~48% at this point at time, signficantly lower than the airlines as a group. This is example of an advanced usage.)\n\n##  Features \n⚕️\tPlanned\n✅ Working \n⚪ Present but not working yet\n\n \n### **Stocks from all over the world**\n \n&nbsp;&nbsp;&nbsp;&nbsp; ✅ Get price history from Interactive Brokers \n\n&nbsp;&nbsp;&nbsp;&nbsp; ✅ Crypto support \n\n&nbsp;&nbsp;&nbsp;&nbsp; ✅ ETF support \n\n### **Connect with your portfolio**\n\n&nbsp;&nbsp;&nbsp;&nbsp; ✅ Export your transactions from [My Stocks Protofolio](https://play.google.com/store/apps/details?id=co.peeksoft.stocks) \n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (Doesn\'t matter which broker you work with)\n\n&nbsp;&nbsp;&nbsp;&nbsp; ✅ Pull transactions data directly from Interactive Brokers TWS. \n\n### **Smart Calculations**\n\n&nbsp;&nbsp;&nbsp;&nbsp; ✅ Adjust Prices and profit relative to a currency. \n\n&nbsp;&nbsp;&nbsp;&nbsp; ✅ Adjust holdings based on stock splits (using stockprices API). \n\n&nbsp;&nbsp;&nbsp;&nbsp; ✅ Combine IB transaction data into MyStocksPortfolio (by exporting csv). \n\n### **Maximum control over graphs**\n\n &nbsp;&nbsp;&nbsp;&nbsp; ✅ Compare performance of group of stocks vs other stock vs your portfolio! \n\n&nbsp;&nbsp;&nbsp;&nbsp; ✅ Many graph types ( Total Profit, Price, Realized Profit, etc...) \n\n&nbsp;&nbsp;&nbsp;&nbsp; ✅ Display percentage change / percentage diff , from certain time / maximum / minimum \n\n&nbsp;&nbsp;&nbsp;&nbsp; ✅ Pick only top stocks for graphs / limit by value range\n\n&nbsp;&nbsp;&nbsp;&nbsp; ✅ Groups of stock can be united by avg price/performance \n\n&nbsp;&nbsp;&nbsp;&nbsp; ✅ Save and load graphs with all parameters instantly! \n\n&nbsp;&nbsp;&nbsp;&nbsp; ⚪ Compare your profit to a theoretical situation in which you have bought the index!\n\n&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp; (the exact same time you have made a purchase)\n\n\n### **Close Integration With Jupyter**\n\n&nbsp;&nbsp;&nbsp;&nbsp; ✅  Display your jupyter notebook with graph! \n\n&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;  i.e. find corelations in your graph (a single line of code. presented by default)\n```\nmydata.act.df.corr(method=\'pearson\')\n```\n\n&nbsp;&nbsp;&nbsp;&nbsp; ✅ Mainipulate data easily in runtime and display graph externally\n\n\n&nbsp;&nbsp;&nbsp;&nbsp; ⚪ Use Jupyter to display graphs inline (if you want) \n```\ngen_graph(Parameters(type=Types.PRICE | Types.COMPARE,compare_with=\'QQQ\',groups=["FANG"],  starthidden=0))\n```\n\n&nbsp;&nbsp;&nbsp;&nbsp; ✅ Edit/reload notebook directly\n\n\n\n\n\n### More\n\n\n✅ Edit categories and groups (using a GUI interface)! \n\n&nbsp;&nbsp;&nbsp;&nbsp;  i.e. Airlines stocks, Growth stocks (Can be compared as a group)\n\n\n✅ **Completely free and open source!** \n\n\n## Planned Features\n\n⚪ Introducing advanced features like P/E and price to sells.\n\n⚪ Get price history from Interactive Brokers \n\n⚕️\tBar graphs (hmmmm, not critical.. ) \n\n⚕️ Adjusted performance based on inflation. \n\n\n\n\n\n⚕️ All this in a web interface!\n\n\n🔴 Not planned - all these technical analysis nonsense..\n\n\n\n## Installation Instructions\n\n\n### For Developers \n\n 1. pip install --no-binary  :all: git+https://github.com/eyalk11/compare-my-stocks.git (or pip install -r requirments.txt)\n 2. Install [Qt6](https://www.qt.io/download) If you want to edit ui file in designer\n\n* Depends on json_editor - https://github.com/eyalk11/json-editor \n\n### For Users\n\n 1. Extract compare-my-stocks.zip from the releases\n\n### For both \nRemark: Really recommended steps, but will work basically without it\n\n 3. Look at myconfig.py and set it as you wish .\n\n    Notice that it is recommended to provide a CSV in MyStocksProtoflio format for every transaction (Type is Buy/Sell):\n 4. Follow the steps for configuring IB \n\n### Remarks \n* **Not fully tested, and prerelease. Some features may not work correctly.** \n* *This program is quite complex and requires non-trivial configuration to work with it properly. I haven\'t got the time to make it completely user-friendly, so I\'d say it requires some developer\'s mentality as things stand now.*\n\n\n## Configuring Interactive Brokers\n \n 1. Run Trader Workstation and sign in (could be readonly).\n   \n 2.  API -> Settings -> Enable ActiveX And Socket Clients\n 3.  Make sure PortIB matches the port in there.\n (   [Here with pictures](https://github.com/eyalk11/compare-my-stocks/wiki/Configurations#configurations-in-trader-workstation) )\n\n\n \n ## Running Instructions\n 1. Run Trader Workstation and sign in (could be readonly). It could be also done after running the app. \n 2. (For developers) python -m compare_my_stocks \n 2. (For users) run compare-my-stocks.exe\n\n\n## Legal Words\n\nI would like to add that: \n\n1. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. That is also true for the any claim associated with usage of Interactive Brokers Api by this code. \n\nPlease consult the corresponding site\'s license before using this software, and use it accordingly. \n\n2. The sofware can use CSVs obtained from using My Stocks Portfolio & Widget by Peeksoft.   \n\n3. This project was developed individually in my free time and without any compensation. I am an in no way affiliated with the mentioned companies. \n\n4. I of course take no responsibilty on the correctness of the displayed graphs/data. \n\n5. Investpy is not supported currently. So you have to have an account in interactive brokers to be able to work properly with it.\n\n## Final words\n* This is being developed in QT with matplotlib amd pandas. I tried to use advanced features of pandas and numpy for fast calculation(sometimes).\n\n* I belive this software provides many useful features that are usually paid for. This despite developing this in a short period, on my spare time. I would very much apperiate community contribution. And welcome you to contribute, send bugs and discuss (will open gitter when appropriate). \n\n* The controls should be self explantory... Try it. \n \n* Feel free to contact me at eyalk5@gmail.com.\n\n',
    'author': 'eyalk5',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
