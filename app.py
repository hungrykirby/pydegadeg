# -*- coding:utf-8 -*-

import twit_utils

tw = twit_utils.Twitter()

if __name__ == "__main__":
    tw.showtimeline()
    tw.streaming()