## Run code guid line
1.run before_install_dependency.sh in ubuntu terminal
```
./before_install_dependency.sh

if you installed dependency run this
./after_install_dependency.sh

```
2.enter necessary values for input
```
eg
    cabinet_cost = 1000
    verge_cost = 50
    road_cost = 100
    chamber_cost = 200
    port_cost = 100
```
3.you will get the result

4.if you need to change "pot" cost calculate with cabinet length then you need to changed .env
```
POT_COST_CALCULATE_DYNAMIC = True
```
## Unit test guide
1. go to project folder and just run "code_test_n_coverage.sh"
```
./code_test_n_coverage.sh

