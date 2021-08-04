import time
import multiprocessing as mp
import signal
from multiprocessing import freeze_support


class CpuTest:

    __wrong_flag = 0

    def test_func(self, s_m):
        # 測試函數,計算斐波那契數列
        if s_m == 's':
            num = 2000000
        else:
            num = 250000
        n1, n2 = 0, 1
        count = 0
        while count < num:
            n3 = n1 + n2
            n1 = n2
            n2 = n3
            count += 1
        return 1

    def multi_task(self):
        # 多核測試，計算1024個250000位的斐波那契數列，統計總耗時
        test_num = 1024  # 多核測試計算數量

        print("多核測試\n計算斐波那契數列中。。。(Ctrl+C退出)")
        num_cores = int(mp.cpu_count())  # cpu核心數
        print("計算機本地有： " + str(num_cores) + " 核心")

        pool = mp.Pool(num_cores, self.del_worker)  # 創建過程池
        result = []
        time0 = time.time()
        for i in range(num_cores):
            result.append(pool.apply_async(self.test_func, args=('m')))

        # 每次向進程池中只添加最多cpu核心數個進程，保證cpu一直滿負荷運行，到1024個斐波那契數列計算完成
        try:
            last_c = 0  # 上一次計算完成數
            while True:
                cur_c = 0  # 當前計算完成數
                for res in result:
                    if res.ready():
                        cur_c += 1
                # print('c: ', cur_c, 'last_c: ', last_c)
                diff_c = cur_c - last_c  # 算完算完的差，就更小一點向劇情添加了一些pu核心數的過程，所以這裡diif_c比cpu核心數還少
                last_c = cur_c
                if diff_c < (test_num - len(result)):  #如果diff_c比現在的流程池裡的流程數與目標數只差，則添加diff_c個流程
                    add_n = diff_c
                else:  # 否則只添加現在過程池裡的過程數與目標數只差那麼幾個，讓計算總數達到目標目標
                    add_n = test_num - len(result)
                for i in range(add_n):
                    # print(add_n, len(result))
                    result.append(pool.apply_async(self.test_func, args=('m')))

                if cur_c == test_num:
                    print(" \nPython CPU多核測試完成耗時： %.3fs" % (time.time() - time0))
                    break

        except KeyboardInterrupt:
            print(" \n主動停止")
            pool.terminate()
            pool.join()
            self.__wrong_flag = 1
            time.sleep(2)

        except Exception as e:
            print(" \n程序錯誤\n", e)
            self.__wrong_flag = 1
            time.sleep(10)

        pool.close()
        pool.join()

    def del_worker(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    def run(self):
        freeze_support()

        flag = ''
        try:
            print(" ")
            flag = input("選擇單核/多核測試(請輸入s/m): ")
            # flag = m
            print(" ")
        except KeyboardInterrupt:
            print(" \n主動退出")
            time.sleep(2)
        except Exception as e:
            print(" \n程序錯誤\n", e)
            time.sleep(10)

        try:
            if flag != 's' and flag != 'm':
                self.__wrong_flag = 1
                print("輸入錯誤！")
                time.sleep(10)
            elif flag == 's':  # 执行单核测试
                print("單核測試\n計算斐波那契數列中。。。(Ctrl+C退出)")
                time0 = time.time()
                self.test_func('s')
                print(" \nPython CPU單核測試完成耗時： %.3fs" % (time.time() - time0))
            else:  # 执行多核测试
                self.multi_task()
            if not self.__wrong_flag:
                print("參考對比：\n"
                       " i7 2600：單核40.053s/多核203.400s\n"
                       " i7 8750H：單核28.693s/多核121.719s\n"
                       " 3400G：單核30.457s/多核162.702s\n"
                       " 3700X：單核28.839s/多核61.854s\n"
                       " 3950X：單核28.065s/多核35.833s\n"
                       " 3990X：單核42.362s/多核14.856s\n"
                       " 樹莓派4b：單核267.841s/多核1015.216s")
                time.sleep(60)
        except KeyboardInterrupt:
            print(" \n主動退出")
            time.sleep(2)
        except Exception as e:
            print(" \n程序錯誤\n", e)
            time.sleep(10)


if __name__ == '__main__':
    test = CpuTest()
    test.run()