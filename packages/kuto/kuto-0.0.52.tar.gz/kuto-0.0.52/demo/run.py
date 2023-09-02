import kuto


if __name__ == '__main__':
    # 执行多个用例文件，主程序入口

    # 执行接口用例
    kuto.main(
        plat="api",
        host='https://app-pre.qizhidao.com',
        path='tests/test_api.py'
    )

    # # 执行安卓用例
    # kuto.main(
    #     plat="android",
    #     did='UJK0220521066836',
    #     pkg='com.qizhidao.clientapp',
    #     path='tests/test_adr.py'
    # )

    # 执行web用例
    # kuto.main(
    #     plat="web",
    #     host='https://www.qizhidao.com/',
    #     path='tests/test_web.py',
    # )
