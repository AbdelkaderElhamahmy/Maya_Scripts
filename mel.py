string $sel[] = `ls -sl`;
for($obj in $sel){
    circle -nr 0 1 0 -ch 0 -n ($obj + "_ctrl");
    group -n ($obj+ "_offsetB");
    group -n ($obj+ "_offsetA");
    group -n ($obj+ "_grp");
    matchTransform ($obj +"_grp") $obj;
    parentConstraint ($obj + "_ctrl")  $obj;
};
$sel = `ls -sl`;
int $i = 0;
for($i = (size($sel));$i >= 0; $i--){
    group -n ($sel[$i] + $sel[$i-1] );
};