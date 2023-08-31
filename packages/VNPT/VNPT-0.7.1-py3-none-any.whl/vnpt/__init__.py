from decimal import Decimal,ROUND_HALF_EVEN# 四舍五入六成双

def round_half_even(value:float, num:int=1)->float:
    """
    对给定的浮点数进行四舍五入操作，并遵循四舍五入六成双的规则。

    Args:
        value (float): 待四舍五入的浮点数。
        num: 保留的小数位数，默认值为1，即保留1位小数。

    Returns:
        float: 四舍五入后的结果。
    """
    return float(Decimal(value).quantize(Decimal(f'{10**(-num)}'), rounding=ROUND_HALF_EVEN))