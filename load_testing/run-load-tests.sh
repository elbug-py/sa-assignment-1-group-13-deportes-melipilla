#!/bin/bash

# Configuración
DOCKER_COMPOSE_FILES=(
    "docker-compose.full.yml"
    "docker-compose.yml"
    "docker-compose.cache.yml" 
    "docker-compose.elastic.yml"
    "docker-compose.app-db-reverse.yml"
)

USER_LOADS=(1 10 100 1000 5000)
TEST_DURATION=300  # 5 minutos
RESULTS_DIR="load_test_results"

# Crear directorio de resultados
mkdir -p $RESULTS_DIR

echo "🚀 Iniciando Load Testing para SA Library"
echo "Duración de cada test: ${TEST_DURATION} segundos (5 minutos)"

# Función para capturar métricas del sistema
capture_metrics() {
    local test_name=$1
    local users=$2
    local compose_file=$3
    
    echo "📊 Capturando métricas para: $test_name"
    
    # Crear directorio específico para este test
    local test_dir="${RESULTS_DIR}/${test_name}_${users}users"
    mkdir -p "$test_dir"
    
    # Capturar métricas de Docker durante el test
    {
        echo "timestamp,container,cpu_percent,memory_usage,memory_limit,memory_percent,network_io,block_io"
        for i in {1..300}; do  # 5 minutos, cada segundo
            timestamp=$(date '+%Y-%m-%d %H:%M:%S')
            docker stats --no-stream --format "table {{.Container}},{{.CPUPerc}},{{.MemUsage}},{{.MemPerc}},{{.NetIO}},{{.BlockIO}}" | tail -n +2 | while IFS=',' read container cpu mem_usage mem_percent net_io block_io; do
                echo "$timestamp,$container,$cpu,$mem_usage,$mem_percent,$net_io,$block_io"
            done
            sleep 1
        done
    } > "$test_dir/docker_metrics.csv" &
    
    local metrics_pid=$!
    
    # Ejecutar JMeter
    jmeter -n -t load-test.jmx \
        -JUSERS=$users \
        -JTEST_DURATION=$TEST_DURATION \
        -JRAMP_TIME=30 \
        -l "$test_dir/jmeter_results.jtl" \
        -e -o "$test_dir/jmeter_report" \
        > "$test_dir/jmeter_log.txt" 2>&1
    
    # Detener captura de métricas
    kill $metrics_pid 2>/dev/null
    
    # Generar resumen
    generate_summary "$test_dir" "$test_name" "$users" "$compose_file"
}

# Función para generar resumen
generate_summary() {
    local test_dir=$1
    local test_name=$2
    local users=$3
    local compose_file=$4
    
    echo "📋 Generando resumen para $test_name"
    
    cat > "$test_dir/summary.txt" << EOF
Load Test Summary
=================
Test Name: $test_name
Users: $users
Duration: $TEST_DURATION seconds
Docker Compose: $compose_file
Timestamp: $(date)

JMeter Results:
EOF
    
    if [ -f "$test_dir/jmeter_results.jtl" ]; then
        # Analizar resultados de JMeter
        awk -F',' 'NR>1 {
            total++; 
            sum_elapsed+=$2; 
            if($8=="true") success++; else failed++;
            if($2>max_time) max_time=$2;
            if(min_time=="" || $2<min_time) min_time=$2;
        } END {
            print "Total Requests: " total
            print "Successful: " success " (" (success/total*100) "%)"
            print "Failed: " failed " (" (failed/total*100) "%)"
            print "Average Response Time: " (sum_elapsed/total) " ms"
            print "Min Response Time: " min_time " ms"
            print "Max Response Time: " max_time " ms"
        }' "$test_dir/jmeter_results.jtl" >> "$test_dir/summary.txt"
    fi
    
    echo "" >> "$test_dir/summary.txt"
    echo "Docker Metrics Summary:" >> "$test_dir/summary.txt"
    
    if [ -f "$test_dir/docker_metrics.csv" ]; then
        # Analizar métricas de Docker (simplificado)
        echo "See docker_metrics.csv for detailed container metrics" >> "$test_dir/summary.txt"
    fi
}

# Función principal de testing
run_test_suite() {
    local compose_file=$1
    local test_name=$(basename "$compose_file" .yml)
    
    echo "🐳 Iniciando tests para: $compose_file"
    
    # Detener servicios existentes
    docker-compose -f "docker/$compose_file" down -v 2>/dev/null
    
    # Iniciar servicios
    echo "⚡ Iniciando servicios..."
    cd docker
    docker-compose -f "$compose_file" up -d --build
    cd ..
    
    # Esperar a que los servicios estén listos
    echo "⏳ Esperando a que los servicios estén listos..."
    sleep 60
    
    # Verificar que la aplicación responde
    if ! curl -f http://localhost:8000/ >/dev/null 2>&1; then
        echo "❌ Error: La aplicación no responde en http://localhost:8000/"
        return 1
    fi
    
    echo "✅ Servicios listos. Iniciando tests de carga..."
    
    # Ejecutar tests para cada nivel de carga
    for users in "${USER_LOADS[@]}"; do
        echo "👥 Testing con $users usuarios..."
        capture_metrics "${test_name}" "$users" "$compose_file"
        
        # Pausa entre tests
        echo "⏸️  Pausa de 30 segundos antes del siguiente test..."
        sleep 30
    done
    
    # Detener servicios
    echo "🛑 Deteniendo servicios..."
    cd docker
    docker-compose -f "$compose_file" down -v
    cd ..
    
    echo "✅ Tests completados para $compose_file"
}

# Verificar dependencias
command -v jmeter >/dev/null 2>&1 || { 
    echo "❌ JMeter no está instalado. Instálalo desde: https://jmeter.apache.org/download_jmeter.cgi"
    echo "En Ubuntu/Debian: sudo apt-get install jmeter"
    echo "En macOS: brew install jmeter"
    exit 1; 
}

command -v docker-compose >/dev/null 2>&1 || { 
    echo "❌ Docker Compose no está instalado."
    exit 1; 
}

# Ejecutar tests para cada configuración de Docker Compose
for compose_file in "${DOCKER_COMPOSE_FILES[@]}"; do
    if [ -f "docker/$compose_file" ]; then
        run_test_suite "$compose_file"
    else
        echo "⚠️  Archivo no encontrado: docker/$compose_file"
    fi
done

echo "🎉 ¡Todos los tests completados!"
echo "📊 Resultados guardados en: $RESULTS_DIR"

# Generar reporte consolidado
echo "📈 Generando reporte consolidado..."
cat > "$RESULTS_DIR/consolidated_report.md" << 'EOF'
# Load Testing Results - SA Library

## Test Configuration
- **Duration**: 5 minutes per test
- **User Loads**: 1, 10, 100, 1000, 5000 concurrent users
- **Ramp-up Time**: 30 seconds
- **Application**: Django + MongoDB

## Docker Compositions Tested
1. **docker-compose.yml** - Basic setup (Django + MongoDB + Envoy)
2. **docker-compose.cache.yml** - With Redis cache + Mesos
3. **docker-compose.elastic.yml** - With Elasticsearch + Mesos  
4. **docker-compose.app-db-reverse.yml** - With reverse proxy

## Results Summary

| Composition | Users | Avg Response Time (ms) | Success Rate (%) | Max CPU (%) | Max Memory (MB) |
|-------------|-------|----------------------|------------------|-------------|-----------------|
EOF

# Agregar resultados al reporte (esto requeriría procesar los archivos generados)
for compose_file in "${DOCKER_COMPOSE_FILES[@]}"; do
    test_name=$(basename "$compose_file" .yml)
    for users in "${USER_LOADS[@]}"; do
        test_dir="${RESULTS_DIR}/${test_name}_${users}users"
        if [ -f "$test_dir/summary.txt" ]; then
            echo "| $test_name | $users | - | - | - | - |" >> "$RESULTS_DIR/consolidated_report.md"
        fi
    done
done

echo "📋 Reporte consolidado generado: $RESULTS_DIR/consolidated_report.md"