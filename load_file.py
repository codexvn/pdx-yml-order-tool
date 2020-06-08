import os
import re
import shutil

count = 0
error_file = []


class YmlProject:
    """存放yml文件的信息"""

    def __init__(self, file_address: str):
        '''通过文件地址加载数据'''

        self._yml_type = ''
        self._yml_data = {}
        self._yml_data_key_sorted = []
        self._yml_file_address = file_address
        if (os.path.getsize(file_address)) < 10:  # 别整个空文件
            error_file.append([self._yml_file_address, '文件太小', 'Size:{}'.format(os.path.getsize(file_address))])
            self.stop = True
            return
        else:
            self.stop = False
        yml_raw_data = ''
        with open(file_address, 'r', encoding='utf-8-sig') as file_point:  # 读取文件数据
            self._yml_type = file_point.readline().encode("utf-8").decode("utf-8-sig")  # 防止多个BOM导致爆炸
            while (len(self._yml_type.lstrip()) == 0 or self._yml_type.lstrip()[0] in ['#', '']):  # 跳过开头的注释和空行
                self._yml_type = file_point.readline()
            for yml_raw_data in file_point.readlines():
                if len(yml_raw_data.lstrip()) == 0 or yml_raw_data.lstrip()[0] in ['#', '']:  # 跳过注释和空行
                    continue
                else:
                    re_data = re.findall(r'([0-9A-Za-z_\.]+:[0-9]*)|(".*\s*")', yml_raw_data)

                    try:
                        self._yml_data[re_data[0][0]] = re_data[1][1]
                    except:
                        error_file.append([self._yml_file_address, re_data, yml_raw_data])
                        self.stop = True
                        # print('re_data)
                        # os._exit(1)
        self._yml_data_key_sorted = sorted(self._yml_data.keys())

    def _PrintData(self):
        for i in self._yml_data.keys():
            print(' {}  {}'.format(i, self._yml_data[i]))
        for i in self._yml_data_key_sorted:
            print(i)

    def _DumpSortedFile(self):
        __dirname = os.path.dirname(self._yml_file_address)
        __basename = os.path.basename(self._yml_file_address)
        # if os.path.exists(os.path.join(__dirname, 'backup')) == False:
        #     os.mkdir(os.path.join(__dirname, 'backup'))
        #
        # if os.path.exists(os.path.join(__dirname, 'backup', __basename)) == True:
        #     os.remove(os.path.join(__dirname, 'backup', __basename))
        # shutil.copyfile(self._yml_file_address, os.path.join(__dirname, 'backup', __basename))
        with open(self._yml_file_address, 'w', encoding='utf-8-sig') as file_point:  # 保存新内容到文件
            file_point.writelines(self._yml_type + '\n')
            for i in self._yml_data_key_sorted:
                file_point.writelines(' {}  {}\n'.format(i, self._yml_data[i]))


def main(dir_address: str):
    """dir_address即翻译文件的目录,该函数会遍历dir_address下的所有yml后缀的文件和子目录下的yml文件"""
    global count
    file_list = []
    walk = os.walk(dir_address)
    for path, dir, file in walk:
        for i in file:
            if (i[-4:] == '.yml'):
                file_list.append(os.path.join(path, i))
    for i in file_list:
        count += 1
        print('Num:{},File:{}'.format(count, i))
        my_yml_project = YmlProject(i)
        #如果要对文件内容排序，这两行就取消注释
        # if (my_yml_project.stop == False):
        #     my_yml_project._DumpSortedFile()
    print('Finshed')
    for i in error_file:
        print('{}  ,  {}\n{}'.format(i[0], i[1], i[2]))


def DumpErrorFileInfo():
    """保存错误文件的数据到当前目录的ErrorMessage.log中"""
    with open(os.path.join(os.getcwd(), 'ErrorMessage.log'), 'w') as f:
        for i in error_file:
            f.writelines('{}  ,  {}\n{}'.format(i[0], i[1], i[2]))


if __name__ == '__main__':
    # 示例
    main('XXX') #这里填文件目录
    DumpErrorFileInfo()
    for i in error_file:
        print(i)
        os.system('code ' + i[0]) #我这里用的vscode，也可以改成你想要的
        pass #改错的话建议在这里下一个断点，然后每次执行到这个断点的时候利用控制台输出的信息改错
    print(len(error_file))
    pass
