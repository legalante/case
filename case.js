// Carregar os dados de retorno acumulado e volatilidade
Promise.all([
    // Faz a requisição dos dados de "retorno_acumulado.json" e converte a resposta em JSON
    fetch("./retorno_acumulado.json").then(response => response.json()),
    // Faz a requisição dos dados de "volatilidade.json" e converte a resposta em JSON
    fetch("./volatilidade.json").then(response => response.json())
])
.then(([retornoData, volatilidadeData]) => {
    // Obter todas as datas de retorno_acumulado
    const datas = Object.keys(retornoData);

    // Preencher os valores de retorno acumulado, usando 0 caso a chave não exista no dado
    const retornos = datas.map(date => retornoData[date]?.retorno_acumulado || 0);
    // Preencher os valores de volatilidade, usando null caso a chave não exista no dado
    const volatilidade = datas.map(date => 
        volatilidadeData[date]?.volatilidade_media || null // Usando null para lacunas
    );

    // Criar o gráfico de Retorno Acumulado utilizando o Plotly
    Plotly.newPlot("retorno-acumulado", [{
        x: datas, // As datas serão o eixo X
        y: retornos, // Os valores de retorno acumulado serão o eixo Y
        type: 'scatter', // Tipo de gráfico de dispersão
        mode: 'lines', // Os dados serão mostrados em formato de linha
        name: 'Retorno Acumulado' // Nome da linha no gráfico
    }]);

    // Criar o gráfico de Volatilidade utilizando o Plotly
    Plotly.newPlot("volatilidade", [{
        x: datas, // As datas serão o eixo X
        y: volatilidade, // Os valores de volatilidade serão o eixo Y
        type: 'scatter', // Tipo de gráfico de dispersão
        mode: 'lines', // Os dados serão mostrados em formato de linha
        name: 'Volatilidade Média' // Nome da linha no gráfico
    }]);
})
// Caso ocorra um erro ao carregar os dados, o erro será exibido no console
.catch(error => console.error('Erro ao carregar os dados:', error));