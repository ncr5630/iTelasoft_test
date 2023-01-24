## Cost calculating guidelines
step one "before_install_dependency.sh" in ubuntu terminal
```
    ./before_install_dependency.sh

    if you installed dependency run this
    ./after_install_dependency.sh

```

step two enter necessary values for input

```
eg
    cabinet_cost = 1000
    verge_cost = 50
    road_cost = 100
    chamber_cost = 200
    port_cost = 100
```
step three you will get final cost for "Rate Card A"

## if you need to calculate "Rate Card B" changed .env
```
POT_COST_CALCULATE_DYNAMIC = True
```
## unit-test guidance
go to project folder and just run "code_test_n_coverage.sh"
```
./code_test_n_coverage.sh

