#!/bin/bash
rm -Rf output/*
rm -Rf plot/*
python analyze.py exp1 @exp1ModelBuild @exp1BestPupil @saccadePlot @windowPlot
python analyze.py exp2 @exp2ModelBuild @saccadePlot @windowPlot
python analyze.py exp1 @crossExpSaccadePlot
python analyze.py exp1 @crossExpWindowPlot
python analyze.py exp3 @exp3ModelBuild @saccadePlot @windowPlot @exp3SaccadePlot
python analyze.py exp3 @exp3WindowPlot