@echo off
setlocal enabledelayedexpansion

REM Configuración
set DOCKER_COMPOSE_FILES=docker-compose.yml docker-compose.cache.yml docker-compose.elastic.yml docker-compose.app-db-reverse.yml
set USER_LOADS=1 10 100 1000 5000
set TEST_DURATION=300
set RESULTS_DIR=load_test_results

REM Crear directorio de resultados
if not exist "%RESULTS_DIR%" mkdir "%RESULTS_DIR%"

echo 🚀 Iniciando Load Testing para SA Library
echo Duración de cada test: %TEST_DURATION% segundos (5 minutos)

REM Verificar dependencias
where jmeter >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ JMeter no está instalado o no está en el PATH
    echo Descarga desde: https://jmeter.apache.org/download_jmeter.cgi
    echo O instala con: choco install jmeter
    exit /b 1
)

where docker-compose >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Docker Compose no está instalado
    exit /b 1
)

REM Función para ejecutar test suite
for %%f in (%DOCKER_COMPOSE_FILES%) do (
    call :run_test_suite "%%f"
)

echo 🎉 ¡Todos los tests completados!
echo 📊 Resultados guardados en: %RESULTS_DIR%

REM Generar reporte consolidado
call :generate_consolidated_report

goto :eof

:run_test_suite
set compose_file=%~1
set test_name=%compose_file:~0,-4%

echo 🐳 Iniciando tests para: %compose_file%

REM Detener servicios existentes
docker-compose -f "docker\%compose_file%" down -v 2>nul

REM Iniciar servicios
echo ⚡ Iniciando servicios...
cd docker
docker-compose -f "%compose_file%" up -d --build
cd ..

REM Esperar a que los servicios estén listos
echo ⏳ Esperando a que los servicios estén listos...
timeout /t 60 /nobreak >nul

REM Verificar que la aplicación responde
curl -f http://localhost:8000/ >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Error: La aplicación no responde en http://localhost:8000/
    goto :continue_next
)

echo ✅ Servicios listos. Iniciando tests de carga...

REM Ejecutar tests para cada nivel de carga
for %%u in (%USER_LOADS%) do (
    echo 👥 Testing con %%u usuarios...
    call :capture_metrics "%test_name%" "%%u" "%compose_file%"
    
    REM Pausa entre tests
    echo ⏸️  Pausa de 30 segundos antes del siguiente test...
    timeout /t 30 /nobreak >nul
)

:continue_next
REM Detener servicios
echo 🛑 Deteniendo servicios...
cd docker
docker-compose -f "%compose_file%" down -v
cd ..

echo ✅ Tests completados para %compose_file%
goto :eof

:capture_metrics
set test_name=%~1
set users=%~2
set compose_file=%~3

echo 📊 Capturando métricas para: %test_name%

REM Crear directorio específico para este test
set test_dir=%RESULTS_DIR%\%test_name%_%users%users
if not exist "%test_dir%" mkdir "%test_dir%"

REM Capturar métricas de Docker durante el test (en background)
start /b cmd /c "call :capture_docker_metrics "%test_dir%""

REM Ejecutar JMeter
jmeter -n -t load_testing\load-test.jmx ^
    -JUSERS=%users% ^
    -JTEST_DURATION=%TEST_DURATION% ^
    -JRAMP_TIME=30 ^
    -l "%test_dir%\jmeter_results.jtl" ^
    -e -o "%test_dir%\jmeter_report" ^
    > "%test_dir%\jmeter_log.txt" 2>&1

REM Generar resumen
call :generate_summary "%test_dir%" "%test_name%" "%users%" "%compose_file%"
goto :eof

:capture_docker_metrics
set test_dir=%~1
set metrics_file=%test_dir%\docker_metrics.csv

echo timestamp,container,cpu_percent,memory_usage,memory_limit,memory_percent,network_io,block_io > "%metrics_file%"

for /l %%i in (1,1,300) do (
    set timestamp=!date! !time!
    
    REM Capturar métricas de Docker (versión simplificada para Windows)
    docker stats --no-stream --format "table {{.Container}},{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}},{{.NetIO}},{{.BlockIO}}" > temp_stats.txt 2>nul
    
    REM Procesar y agregar timestamp (simplificado)
    for /f "skip=1 tokens=*" %%a in (temp_stats.txt) do (
        echo !timestamp!,%%a >> "%metrics_file%"
    )
    
    timeout /t 1 /nobreak >nul
)

del temp_stats.txt 2>nul
goto :eof

:generate_summary
set test_dir=%~1
set test_name=%~2
set users=%~3
set compose_file=%~4

echo 📋 Generando resumen para %test_name%

(
echo Load Test Summary
echo =================
echo Test Name: %test_name%
echo Users: %users%
echo Duration: %TEST_DURATION% seconds
echo Docker Compose: %compose_file%
echo Timestamp: %date% %time%
echo.
echo JMeter Results:
) > "%test_dir%\summary.txt"

if exist "%test_dir%\jmeter_results.jtl" (
    REM Análisis básico de JMeter (versión simplificada para Windows)
    echo Analyzing JMeter results... >> "%test_dir%\summary.txt"
    echo See jmeter_results.jtl for detailed results >> "%test_dir%\summary.txt"
)

echo. >> "%test_dir%\summary.txt"
echo Docker Metrics Summary: >> "%test_dir%\summary.txt"

if exist "%test_dir%\docker_metrics.csv" (
    echo See docker_metrics.csv for detailed container metrics >> "%test_dir%\summary.txt"
)
goto :eof

:generate_consolidated_report
echo 📈 Generando reporte consolidado...

(
echo # Load Testing Results - SA Library
echo.
echo ## Test Configuration
echo - **Duration**: 5 minutes per test
echo - **User Loads**: 1, 10, 100, 1000, 5000 concurrent users
echo - **Ramp-up Time**: 30 seconds
echo - **Application**: Django + MongoDB
echo.
echo ## Docker Compositions Tested
echo 1. **docker-compose.yml** - Basic setup ^(Django + MongoDB + Envoy^)
echo 2. **docker-compose.cache.yml** - With Redis cache + Mesos
echo 3. **docker-compose.elastic.yml** - With Elasticsearch + Mesos  
echo 4. **docker-compose.app-db-reverse.yml** - With reverse proxy
echo.
echo ## Results Summary
echo.
echo ^| Composition ^| Users ^| Avg Response Time ^(ms^) ^| Success Rate ^(%%^) ^| Max CPU ^(%%^) ^| Max Memory ^(MB^) ^|
echo ^|-------------|-------|----------------------|------------------|-------------|-----------------|
) > "%RESULTS_DIR%\consolidated_report.md"

for %%f in (%DOCKER_COMPOSE_FILES%) do (
    set test_name=%%f
    set test_name=!test_name:~0,-4!
    for %%u in (%USER_LOADS%) do (
        set test_dir=%RESULTS_DIR%\!test_name!_%%uusers
        if exist "!test_dir!\summary.txt" (
            echo ^| !test_name! ^| %%u ^| - ^| - ^| - ^| - ^| >> "%RESULTS_DIR%\consolidated_report.md"
        )
    )
)

echo 📋 Reporte consolidado generado: %RESULTS_DIR%\consolidated_report.md
goto :eof