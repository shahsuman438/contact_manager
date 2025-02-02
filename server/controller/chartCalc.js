function chartCalc(data) {
    const chartData = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].map(day => ({ name: day, Total: 0 }));
    
    const sixDaysAgo = new Date();
    sixDaysAgo.setDate(sixDaysAgo.getDate() - 7);
    
    const counts = data
        .filter(item => new Date(item.created) > sixDaysAgo)
        .reduce((acc, item) => {
            const day = new Date(item.created).toLocaleString('en-us', { weekday: 'long' });
            acc[day] = (acc[day] || 0) + 1;
            return acc;
        }, {});
    
    chartData.forEach(item => item.Total = counts[item.name] || 0);
    
    return sort(chartData);
}
