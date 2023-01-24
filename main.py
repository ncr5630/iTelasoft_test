from broadband_cost import BroadBandCost

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cabinet_cost = 100
    verge_cost = 100
    road_cost = 100
    chamber_cost = 1002
    port_cost = 20

    # cabinet_cost = float(input("Insert single Cabinet cost :"))
    # verge_cost = float(input("\nInsert 1 meter verge cost :"))
    # road_cost = float(input("\nInsert 1 meter road cost :"))
    # chamber_cost = float(input("\nInsert single chamber cost :"))
    # port_cost = float(input("\nInsert single port cost :"))

    cost_oj = BroadBandCost(cabinet_cost, verge_cost, road_cost, chamber_cost, port_cost)
    total_cost = cost_oj.final_cost()

    print(f"\nTotal cost with given data : {total_cost}")
