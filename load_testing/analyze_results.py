#!/usr/bin/env python3
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

def analyze_jmeter_results(jtl_file):
    """Analiza los resultados de JMeter"""
    try:
        # Leer archivo JTL de JMeter
        df = pd.read_csv(jtl_file)
        
        # Calcular métricas
        total_requests = len(df)
        successful_requests = len(df[df['success'] == True])
        failed_requests = total_requests - successful_requests
        success_rate = (successful_requests / total_requests) * 100
        
        # Tiempos de respuesta
        avg_response_time = df['elapsed'].mean()
        min_response_time = df['elapsed'].min()
        max_response_time = df['elapsed'].max()
        p95_response_time = df['elapsed'].quantile(0.95)
        p99_response_time = df['elapsed'].quantile(0.99)
        
        return {
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': failed_requests,
            'success_rate': success_rate,
            'avg_response_time': avg_response_time,
            'min_response_time': min_response_time,
            'max_response_time': max_response_time,
            'p95_response_time': p95_response_time,
            'p99_response_time': p99_response_time
        }
    except Exception as e:
        print(f"Error analyzing {jtl_file}: {e}")
        return None

def analyze_docker_metrics(csv_file):
    """Analiza las métricas de Docker"""
    try:
        df = pd.read_csv(csv_file)
        
        # Limpiar datos de CPU (remover %)
        df['cpu_clean'] = df['cpu_percent'].str.replace('%', '').astype(float)
        
        # Procesar memoria (extraer números)
        df['memory_usage_mb'] = df['memory_usage'].str.extract('(\d+\.?\d*)').astype(float)
        df['memory_percent_clean'] = df['memory_percent'].str.replace('%', '').astype(float)
        
        # Calcular métricas por contenedor
        container_metrics = {}
        for container in df['container'].unique():
            container_data = df[df['container'] == container]
            container_metrics[container] = {
                'avg_cpu': container_data['cpu_clean'].mean(),
                'max_cpu': container_data['cpu_clean'].max(),
                'avg_memory_mb': container_data['memory_usage_mb'].mean(),
                'max_memory_mb': container_data['memory_usage_mb'].max(),
                'avg_memory_percent': container_data['memory_percent_clean'].mean(),
                'max_memory_percent': container_data['memory_percent_clean'].max()
            }
        
        return container_metrics
    except Exception as e:
        print(f"Error analyzing {csv_file}: {e}")
        return None

def generate_comprehensive_report():
    """Genera un reporte comprehensive de todos los tests"""
    results_dir = Path("load_test_results")
    
    if not results_dir.exists():
        print("No se encontró el directorio de resultados")
        return
    
    all_results = []
    
    # Procesar cada directorio de test
    for test_dir in results_dir.iterdir():
        if not test_dir.is_dir() or test_dir.name == "__pycache__":
            continue
            
        print(f"Procesando: {test_dir.name}")
        
        # Extraer información del nombre del directorio
        parts = test_dir.name.split('_')
        if len(parts) >= 2:
            composition = '_'.join(parts[:-1])
            users = parts[-1].replace('users', '')
        else:
            continue
        
        # Analizar resultados de JMeter
        jtl_file = test_dir / "jmeter_results.jtl"
        jmeter_results = None
        if jtl_file.exists():
            jmeter_results = analyze_jmeter_results(jtl_file)
        
        # Analizar métricas de Docker
        docker_file = test_dir / "docker_metrics.csv"
        docker_results = None
        if docker_file.exists():
            docker_results = analyze_docker_metrics(docker_file)
        
        # Consolidar resultados
        result = {
            'composition': composition,
            'users': int(users),
            'jmeter': jmeter_results,
            'docker': docker_results
        }
        all_results.append(result)
    
    # Generar reporte HTML
    generate_html_report(all_results)
    
    # Generar gráficos
    generate_charts(all_results)
    
    print("✅ Reporte comprehensive generado")

def generate_html_report(results):
    """Genera un reporte HTML detallado"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SA Library Load Test Results</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
            th { background-color: #f2f2f2; }
            .composition { background-color: #e8f4fd; }
            .metric-good { color: green; font-weight: bold; }
            .metric-warning { color: orange; font-weight: bold; }
            .metric-bad { color: red; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>SA Library Load Test Results</h1>
        <h2>Performance Summary</h2>
        <table>
            <tr>
                <th>Composition</th>
                <th>Users</th>
                <th>Total Requests</th>
                <th>Success Rate (%)</th>
                <th>Avg Response Time (ms)</th>
                <th>P95 Response Time (ms)</th>
                <th>Max CPU (%)</th>
                <th>Max Memory (MB)</th>
            </tr>
    """
    
    for result in sorted(results, key=lambda x: (x['composition'], x['users'])):
        jmeter = result.get('jmeter', {})
        
        # Calcular CPU y memoria máxima de todos los contenedores
        max_cpu = 0
        max_memory = 0
        if result.get('docker'):
            for container, metrics in result['docker'].items():
                max_cpu = max(max_cpu, metrics.get('max_cpu', 0))
                max_memory = max(max_memory, metrics.get('max_memory_mb', 0))
        
        # Aplicar clases CSS basadas en performance
        success_rate = jmeter.get('success_rate', 0)
        avg_response = jmeter.get('avg_response_time', 0)
        
        success_class = "metric-good" if success_rate >= 95 else ("metric-warning" if success_rate >= 85 else "metric-bad")
        response_class = "metric-good" if avg_response <= 1000 else ("metric-warning" if avg_response <= 3000 else "metric-bad")
        
        html_content += f"""
            <tr>
                <td class="composition">{result['composition']}</td>
                <td>{result['users']}</td>
                <td>{jmeter.get('total_requests', 'N/A')}</td>
                <td class="{success_class}">{success_rate:.2f}</td>
                <td class="{response_class}">{avg_response:.2f}</td>
                <td>{jmeter.get('p95_response_time', 'N/A'):.2f}</td>
                <td>{max_cpu:.2f}</td>
                <td>{max_memory:.2f}</td>
            </tr>
        """
    
    html_content += """
        </table>
        
        <h2>Detailed Container Metrics</h2>
        <p>Check the generated charts for detailed performance analysis.</p>
        
        <h2>Test Configuration</h2>
        <ul>
            <li>Test Duration: 5 minutes per test</li>
            <li>Ramp-up Time: 30 seconds</li>
            <li>User Loads: 1, 10, 100, 1000, 5000</li>
            <li>Application: Django + MongoDB</li>
        </ul>
        
        <h2>Recommendations</h2>
        <ul>
            <li><strong>Green metrics:</strong> Excellent performance</li>
            <li><strong>Orange metrics:</strong> Acceptable but monitor closely</li>
            <li><strong>Red metrics:</strong> Performance issues detected</li>
        </ul>
    </body>
    </html>
    """
    
    with open("load_test_results/comprehensive_report.html", "w") as f:
        f.write(html_content)

def generate_charts(results):
    """Genera gráficos de performance"""
    # Configurar estilo
    plt.style.use('seaborn')
    sns.set_palette("husl")
    
    # Crear DataFrame para análisis
    data = []
    for result in results:
        if result.get('jmeter'):
            jmeter = result['jmeter']
            data.append({
                'composition': result['composition'],
                'users': result['users'],
                'success_rate': jmeter.get('success_rate', 0),
                'avg_response_time': jmeter.get('avg_response_time', 0),
                'p95_response_time': jmeter.get('p95_response_time', 0),
                'total_requests': jmeter.get('total_requests', 0)
            })
    
    df = pd.DataFrame(data)
    
    if df.empty:
        print("No hay datos para generar gráficos")
        return
    
    # Gráfico 1: Tiempo de respuesta vs Usuarios
    plt.figure(figsize=(12, 8))
    for comp in df['composition'].unique():
        comp_data = df[df['composition'] == comp]
        plt.plot(comp_data['users'], comp_data['avg_response_time'], 
                marker='o', label=f'{comp} (Avg)', linewidth=2)
        plt.plot(comp_data['users'], comp_data['p95_response_time'], 
                marker='s', label=f'{comp} (P95)', linestyle='--', alpha=0.7)
    
    plt.xlabel('Concurrent Users')
    plt.ylabel('Response Time (ms)')
    plt.title('Response Time vs User Load')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig('load_test_results/response_time_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Gráfico 2: Success Rate vs Usuarios
    plt.figure(figsize=(12, 6))
    for comp in df['composition'].unique():
        comp_data = df[df['composition'] == comp]
        plt.plot(comp_data['users'], comp_data['success_rate'], 
                marker='o', label=comp, linewidth=2)
    
    plt.xlabel('Concurrent Users')
    plt.ylabel('Success Rate (%)')
    plt.title('Success Rate vs User Load')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xscale('log')
    plt.ylim(0, 105)
    plt.axhline(y=95, color='r', linestyle='--', alpha=0.7, label='95% threshold')
    plt.savefig('load_test_results/success_rate_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("📊 Gráficos generados en load_test_results/")

if __name__ == "__main__":
    generate_comprehensive_report()