import numpy as np



class ReadRaw:
    def __init__(self):
        pass

    @staticmethod
    def read_file(file_name):
        with open(file_name, 'rb') as f:
            # 分别读取头文件，跳过第一行
            use_data = next(f).replace(b'\n', b'').strip().split(b'|')[1:]

            # 初始化变量
            byte_len = 0
            sample_dt = ''
            channel_num = 0
            CH_name = ''
            Calib_coef = 0
            dat_unit = ''

            #开始分析
            for c in use_data:
                # 切分
                use_c = c[:-1].split(b',')
                if c.startswith(b'CN'):
                    # 通道数量 CF标识的个数
                    channel_num += 1
                    # 通道名称
                    CH_name = use_c[7]

                if c.startswith(b'CD'):
                    sample_dt = use_c[3]
                    sample_unit = use_c[6]

                if c.startswith(b'Cb'):
                    block_size = int(use_c[8])

                if c.startswith(b'CR'):
                    Calib_coef = use_c[4]
                    dat_unit = use_c[8].decode('gb2312')

                if c.startswith(b'CP'):
                    byte_len = int(use_c[4])

        with open(file_name, 'rb') as f:
            run_id = True
            while run_id:
                if f.read(1) == b'|':
                    if f.read(2) == b'CS':
                        run_id = False

            run_id_2 = True
            comma_sum = 0
            while run_id_2:
                if comma_sum < 4:
                    if f.read(1) == b',':
                        comma_sum += 1
                else:
                    run_id_2 = False

            #判定编码
            if byte_len == 2:
                dat_type = 'int16'
            elif byte_len == 8:
                dat_type = np.float64
            elif byte_len == 4:
                dat_type = np.float32


            # 读取数据
            dat_block = np.fromfile(f, dtype=dat_type, count=int(block_size/byte_len))

        # 灵敏度系数计算
        # 判断是否是0
        if Calib_coef != b'0':
            try:
                dat_raw = dat_block * round(float(Calib_coef), 4)
            except ValueError:
                dat_raw = dat_block
        else:
            dat_raw = dat_block

        return CH_name, dat_unit, np.asarray(list(dat_raw)), sample_dt