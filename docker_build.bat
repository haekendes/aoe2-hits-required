@ECHO OFF

docker buildx build --platform linux/amd64,linux/arm/v7 -t haekendes/aoe2_unit_breakpoints --push  .

REM docker pull haekendes/aoe2_unit_breakpoints

exit