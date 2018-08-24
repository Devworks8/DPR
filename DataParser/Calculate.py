import sympy as spy


class Calculate:
    def __init__(self):
        pass

    def convert(self, data=None, reverse=False):
        """
        Convert any string representation of a rational to a mix rational with the denominator maintained in 8th
        :param data:
        :param reverse:
        :return: String of mix rational
        """
        value = ''
        if isinstance(data, spy.Rational) or len(data) > 0:
            if reverse is False:
                rational = spy.Rational(data)
                if rational.q is not 8:
                    if rational.q > 8:
                        f = int(rational.q / 8)
                        rational.p = rational.p / f
                        rational.q = rational.q / f
                        if rational.p > 8:
                            value.format("%d %d", rational.p / 8, rational.p % 8)
                    elif rational.q == 1:
                        value = rational
                    else:
                        f = int(8 / rational.q)
                        rational.p = rational.p * f
                        rational.q = rational.q * f
                        value = rational
                        if rational.p > 8:
                            str(value).format("%d %d", rational.p / 8, rational.p % 8)
                else:
                    if int(rational.p) > 8:

                        value = '%d %d/%d' % (rational.p // rational.q, rational.p % rational.q, rational.q)
                    else:
                        value = rational
            else:
                if len(data) > 4:
                    breakdown = data.split(' ')
                    value = spy.sympify(breakdown[0]+'+'+breakdown[1])
        else:
            pass

        return str(value)

    def formatData(self, data, template):
        fmtData = [[]]

        if len(data) == 0:
            return
        fmtData[0].append(data[0])

        fmtData.append([])
        for index in range(1, 8):
            fmtData[len(fmtData)-1].append(data[index])

        for index in range(9, 129):
            if len(fmtData[len(fmtData) - 1]) % 7 == 0:
                fmtData.append([data[index]])
            elif len(fmtData[len(fmtData) - 1]) % 6 == 0:
                fmtData.append([data[index]])
            else:
                fmtData[len(fmtData) - 1].append(data[index])

        fmtData.append([])
        for index in range(130, 136):
            fmtData[len(fmtData)-1].append(data[index])

        fmtData.append(template)

        fmtData.append([])
        fmtData[len(fmtData)-1].append(data[161])

        return fmtData

    def process(self, d1, d2):
        # pass to the convert method to convert to mixed rational, and vice versa
        x = spy.symbols('x')

        if d1 == "" or d2 == "":
            return ""

        x = spy.sympify("{} + {}".format(d1, d2), rational=True)

        return x