function generateCoordinate(x, y) {
    return {
        "a": +x,
        "o": +y,
        "v": 1,
        "s": 0,
        "t": 0,
        "ac": 0
    };
}

function generateData() {
    var odometer = (3 + Math.random() / 3).toFixed(2);
    var minutes = 15 + Math.random() * 10;
    var activeTime = "00:" + padZero(minutes) + ":" + padZero((minutes % 1) * 60);
    var calorie = +(320 / 30 * minutes).toFixed(1);
    var speed = odometer / minutes * 60;
    var avgSpeed = speed.toFixed(2);
    var maxSpeed = (speed + 0.5 + Math.random() * 0.7).toFixed(2);
    var now = Date.now();
    var beginTime = (new Date(now - minutes * 60000 - new Date().getTimezoneOffset() * 60000)).toISOString().split('.')[0].replace('T', ' ');
    var endTime = (new Date(now - new Date().getTimezoneOffset() * 60000)).toISOString().split('.')[0].replace('T', ' ');
    var isValid = 1;
    var isValidReason = "";
    var stepCount = ~~(3000 + Math.random() * 1000);
    var minutesPerKM = minutes / odometer;
    var pace = [
        {
            km: "1",
            t: padZero(minutesPerKM - Math.random() * 1.5) + "'" + padZero(Math.random() * 60) + "''"
        },
        {
            km: "2",
            t: padZero(minutesPerKM) + "'" + padZero(Math.random() * 60) + "''"
        },
        {
            km: "3",
            t: padZero(minutesPerKM + Math.random() * 1.5) + "'" + padZero(Math.random() * 60) + "''"
        }
    ];
    var minuteSpeed = [];
    for (var i = 1; i <= minutes; i++) {
        minuteSpeed.push({
            min: i,
            v: (speed + Math.random() * (i < minutes / 2 ? 1 : -1)).toFixed(2)
        })
    }
    var minSpeedPerHour = (speed - 0.5 - Math.random() * 0.7).toFixed(2);
    var maxSpeedPerHour = (maxSpeed - Math.random() * 0.4).toFixed(2);
    var avgPace = padZero(minutesPerKM) + "'" + padZero(Math.random() * 60) + "''";
    var lastOdometerTime = "00:" + padZero(minutesPerKM + Math.random() * 1.5) + ":" + padZero(Math.random() * 60);
    var stepMinute = (stepCount / minutes).toFixed(2);
    var beganX = (30.508 + Math.random() / 10e2).toFixed(6);
    var beganY = (114.408 + Math.random() / 10e2).toFixed(6);
    var beganPoint = beganX + "|" + beganY;
    var endX = (30.514 + Math.random() / 10e2).toFixed(6);
    var endY = (114.432 + Math.random() / 10e2).toFixed(6);
    var endPoint = endX + "|" + endY;
    var points = ["30.509, 114.408", "30.511, 114.408", "30.511, 114.410", "30.510, 114.416", "30.510, 114.420", "30.513, 114.421", "30.515, 114.421", "30.514, 114.427", "30.514, 114.430"];
    var coordinate = [];
    coordinate.push(generateCoordinate(beganX, beganY));
    for (var i = 0; i < points.length; i++) {
        var point = points[i].split(', ');
        var x = +point[0] + Math.random() / 10e2;
        var y = +point[1] + Math.random() / 10e2;
        coordinate.push(generateCoordinate(x, y));
    }
    coordinate.push(generateCoordinate(endX, endY));
    return {
        calorie: calorie,
        odometer: odometer,
        avgSpeed: avgSpeed,
        activeTime: activeTime,
        beginTime: beginTime,
        endTime: endTime,
        isValid: isValid,
        isValidReason: isValidReason,
        stepCount: stepCount,
        pace: pace,
        minuteSpeed: minuteSpeed,
        minSpeedPerHour: minSpeedPerHour,
        maxSpeedPerHour: maxSpeedPerHour,
        avgPace: avgPace,
        lastOdometerTime: lastOdometerTime,
        stepMinute: stepMinute,
        beganPoint: beganPoint,
        endPoint: endPoint,
        coordinate: coordinate
    };
}
