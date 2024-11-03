const customBGColorCode = document.getElementById("background_color").textContent
console.log("bgcolor: "+customBGColorCode)
let colorRegEx = /^[#]{1}[A-F0-9a-f]{6}$/
if (colorRegEx.test(customBGColorCode)) document.body.style.backgroundColor = customBGColorCode;
else if (customBGColorCode == "random")
{
    const BGColors = ["#f7ffff", "#fff7ff", "#fffff7", "#f7f7ff", "#f7fff7", "#f7f7ff", "#f7f7f7", "#ffffff"];
    document.body.style.backgroundColor = BGColors[Math.floor(Math.random() * BGColors.length)];
}
else document.body.style.backgroundColor = "#FFFFFF";