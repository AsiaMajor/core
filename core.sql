CREATE TABLE TrainingData(
    sheetNumber INT,
    iteration INT,
    avgMoe FLOAT,
    avgSG FLOAT,
    avgMC FLOAT,
    AvgVel FLOAT,
    AvgUPT FLOAT,
    Width FLOAT,
    Skew FLOAT,
    AvgThick FLOAT,
    Temp FLOAT,
    PkMoisture FLOAT,
    pkDensity FLOAT

    PRIMARY KEY (sheetNumber, iteration)
);

CREATE TABLE TestingData(
    sheetNumber INT,
    iteration INT,
    avgMoe FLOAT,
    avgSG FLOAT,
    avgMC FLOAT,
    AvgVel FLOAT,
    AvgUPT FLOAT,
    Width FLOAT,
    Skew FLOAT,
    AvgThick FLOAT,
    Temp FLOAT,
    PkMoisture FLOAT,
    pkDensity FLOAT

    PRIMARY KEY (sheetNumber, iteration)
);