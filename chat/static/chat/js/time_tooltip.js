function updTimeTooltip()
{
    const timeContainers = document.querySelectorAll('.time-container');

    timeContainers.forEach(container => {
        const tooltip = container.querySelector('.tooltip');

        container.addEventListener('mouseenter', function() {
            tooltip.style.display = 'block'; // 显示提示框
        });

        container.addEventListener('mousemove', function(e) {
            // 动态更新提示框的位置
            tooltip.style.left = (e.offsetX + 10) + 'px';
            tooltip.style.top = (e.offsetY + 10) + 'px';
        });

        container.addEventListener('mouseleave', function() {
            tooltip.style.display = 'none'; // 隐藏提示框
        });
    });
}