//
//  Charts.swift
//  URApp
//
//  Created by XavierRoma on 17/03/2019.
//  Copyright © 2019 x.roma_gabriel.cammany. All rights reserved.
//

import UIKit
import SceneKit
import ARKit
import ARCharts

class ChartCreator {
    
    private static let arKitColors = [
        UIColor(red: 238.0 / 255.0, green: 109.0 / 255.0, blue: 150.0 / 255.0, alpha: 1.0),
        UIColor(red: 70.0  / 255.0, green: 150.0 / 255.0, blue: 150.0 / 255.0, alpha: 1.0),
        UIColor(red: 134.0 / 255.0, green: 218.0 / 255.0, blue: 255.0 / 255.0, alpha: 1.0),
        UIColor(red: 237.0 / 255.0, green: 231.0 / 255.0, blue: 254.0 / 255.0, alpha: 1.0),
        UIColor(red: 0.0   / 255.0, green: 110.0 / 255.0, blue: 235.0 / 255.0, alpha: 1.0),
        UIColor(red: 193.0 / 255.0, green: 193.0 / 255.0, blue: 255.0 / 255.0, alpha: 1.0),
        UIColor(red: 84.0  / 255.0, green: 204.0 / 255.0, blue: 254.0 / 255.0, alpha: 1.0)
    ]
    
    private static func setupGraph(barChart: ARBarChart) {
        barChart.animationType = .fade
        barChart.size = SCNVector3(0.2, 0.2, 0.2)
    }
    
    static func createBarChart(at position: SCNVector3, seriesLabels: Array<String>, indexLabels: Array<String>, values: [[Double]]) -> ARBarChart {
        //let values = generateRandomNumbers(withRange: 0..<50, numberOfRows: 2, numberOfColumns: 2)
        //let seriesLabels = Array(0..<values.count).map({ "Series \($0)" })
        //let indexLabels = Array(0..<values.first!.count).map({ "Index \($0)" })
        let dataSeries = ARDataSeries(withValues: values)
        
        dataSeries.seriesLabels = seriesLabels
        dataSeries.indexLabels = indexLabels
        dataSeries.spaceForIndexLabels = 0.2
        dataSeries.spaceForIndexLabels = 0.2
        
        dataSeries.barColors = arKitColors
        dataSeries.barOpacity = 40
        
        let barChart = ARBarChart()
        barChart.dataSource = dataSeries
        barChart.delegate = dataSeries
        self.setupGraph(barChart: barChart)
        barChart.position = position
        barChart.draw()
        return barChart
    }
    
}
