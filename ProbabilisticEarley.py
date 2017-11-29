import time
from rules import rules
from probability import prob

#main function
def main():

    #input_arr = 'Every dog loves Fido'.split() + [""]
    input_arr = 'the man saw the dog with the telescope'.split() + [""]
    print('START TIME: {0}'.format(time.clock()))
    for curr_state in range(len(input_arr)):
        curr_chart = charts[curr_state]
        next_chart = []

        for curr_rule in curr_chart:
            #check whether complete or not
            if curr_rule["dot"] < len(curr_rule["rhs"]):
                for i in predictor(curr_rule, curr_state):
                    isUpdated = 0
                    for temp_rule in curr_chart:
                        if i["rhs"] == temp_rule["rhs"] and i["lhs"] == temp_rule["lhs"] and i["dot"] == temp_rule["dot"]:
                            isUpdated = 1
                    if isUpdated == 0:
                        curr_chart += [i]
                for i in scanner(curr_rule, input_arr[curr_state]):
                    if i not in next_chart:
                        next_chart += [i]
            else:
                for i in completor(curr_rule, charts):
                    isUpdated = 0
                    for temp_rule in curr_chart:
                        if i["rhs"] == temp_rule["rhs"] and i["lhs"] == temp_rule["lhs"] and i["dot"] == temp_rule["dot"]:
                            if i["probability"] > temp_rule["probability"]:
                                temp_rule["probability"] = i["probability"]
                                temp_rule["completor"] = i["completor"]
                            isUpdated = 1
                    if isUpdated == 0:
                        curr_chart += [i]


        charts.append(next_chart)
    print('END TIME: {0}'.format(time.clock()))

    print_charts(charts[:-1], input_arr)
    parse(charts[-2])


#Chart Iniitialization
charts = [[{
    "lhs": "ROOT",
    "rhs": ["S"],
    "dot": 0,
    "state": 0,
    "end" : 0,
    "op": "DUMMY",
    "completor": [],
    "probability" : 1.0
}]]

#Predictor Function
def predictor(rule, state):
    return [{
        "lhs": rule["rhs"][rule["dot"]],
        "rhs": rhs,
        "dot": 0,
        "state": state,
        "end" : state,
        "op": "PREDICTOR",
        "completor": [],
        "probability" : prob[rule["rhs"][rule["dot"]]][index][0]
    } for index,rhs in enumerate(rules[rule["rhs"][rule["dot"]]])] if rule["rhs"][rule["dot"]].isupper() else []

#Scanner Function
def scanner(rule, next_input):
    return [{
        "lhs": rule["rhs"][rule["dot"]],
        "rhs": [next_input],
        "dot": 1,
        "state": rule["end"],
        "end" : rule["end"] + 1,
        "op": "SCANNER",
        "completor": [],
        "probability": prob[rule["rhs"][rule["dot"]]][next_input]
    }] if rule["rhs"][rule["dot"]].islower() and next_input in rules[rule["rhs"][rule["dot"]]] else []

#Completer Function
def completor(rule, charts):
    return list(map(
        lambda filter_rule: {
            "lhs": filter_rule["lhs"],
            "rhs": filter_rule["rhs"],
            "dot": filter_rule["dot"]+1,
            "state": filter_rule["state"],
            "end" : rule["end"],
            "op": "COMPLETOR",
            "completor": [rule] + filter_rule["completor"],
            "probability": rule["probability"]*filter_rule["probability"]
        },
        filter(
            lambda p_rule: p_rule["dot"] < len(p_rule["rhs"]) and rule["lhs"] == p_rule["rhs"][p_rule["dot"]],
            charts[rule["state"]]
        )
    )) if (rule["dot"]) == len(rule["rhs"]) else []

#Print Charts
def print_charts(charts, inp):
    print("\n\n\n\tCHARTS")
    for chart_no, chart in zip(range(len(charts)), charts):
        print("\n\n\n\t{0:^84}".format("CHART " + str(chart_no)))
        print("\t{0:-^84}".format(""))
        print("\t|{0:^82}|".format(" ".join(inp[:chart_no] + ["."] + inp[chart_no:])))
        print("\t{0:-<84}".format(""))
        print("\t|{0:^35}|{1:^20}|{2:^25}|".format("PRODUCTION", "[STATE, END]", "OPERATION"))
        print("\t{0:-<84}".format(""))
        print("\t\n".join(map(
            lambda x: "\t| {0:>10} --> {1:<19}|{2:^20}|{3:^25}|".format(
                x["lhs"],
                " ".join(x["rhs"][:x["dot"]] + ["."] + x["rhs"][x["dot"]:]),
                "[" + str(x["state"]) + "," + str(x["end"]) + "]",
                x["op"]
            ),
            chart
        )))
        print("\t{0:-<84}".format(""))

#Print Parse Tree
def parse(chart):
    tree = [ rule for rule in chart if rule["dot"] == len(rule["rhs"]) and rule["lhs"] == "ROOT" ]
    for p in range(len(tree)):
        rules, stack = [], [tree[p]]
        print("\n\nPath{0}:".format(p))
        print("\n")

        while len(stack) > 0:
            curr_node = stack.pop()

            rules.append("\t| {0:>10} --> {1:<19}|    {2:>10}".format(curr_node["lhs"], " ".join(curr_node["rhs"]), curr_node["probability"]))

            stack.extend([ i for i in curr_node["completor"] ])

        #print("\n\t")
        print("\t{0:-^37}".format(""))
        print("\t|{0:^35}|".format("RESULT"))
        print("\t{0:-^37}".format(""))
        print("\n".join(rules))
        print("\t{0:-^37}".format(""))


if __name__ == "__main__":
    main()