//
//  Utilities.swift
//  URApp
//
//  Created by XavierRoma on 17/03/2019.
//  Copyright © 2019 x.roma_gabriel.cammany. All rights reserved.
//

import Foundation


func generateRandomNumbers(withRange range: Range<Int>, numberOfRows rowCount: Int, numberOfColumns columnCount: Int) -> [[Double]] {
    guard rowCount > 0 && columnCount > 0 else {
        return [[0]]
    }
    
    var columnCount = columnCount
    var numbers = [[Double]]()
    while columnCount > 0 {
        numbers.append(generateRandomNumbers(withRange: range, count: rowCount))
        columnCount -= 1
    }
    
    return numbers
}

func generateRandomNumbers(withRange range: Range<Int>, count: Int) -> [Double] {
    var count = count
    var numbers = [Double]()
    while count > 0 {
        numbers.append(generateRandomNumber(withRange: range))
        count -= 1
    }
    
    return numbers
}

func generateRandomNumber(withRange range: Range<Int>) -> Double {
    return Double(arc4random_uniform(UInt32(range.upperBound - range.lowerBound))) + Double(range.lowerBound)
}

func generateNumbers(fromDataSampleWithIndex index: Int) -> [[Double]]? {
    let resourceName = String(format: "DataSample_%i", index)
    
    guard let dataPath = Bundle.main.path(forResource: resourceName, ofType: "csv") else {
        print(String(format: "Could Not Load Data Sample File %@", resourceName))
        return nil
    }
    
    var data = [[Double]]()
    if let dataSampleString = try? String(contentsOfFile: dataPath) {
        let lines = dataSampleString.components(separatedBy: "\n")
        let headerEntries = lines[0].components(separatedBy: ",")
        for line in lines[1...] {
            let lineEntries = line.components(separatedBy: ",")
            if lineEntries.count == headerEntries.count {
                data.append(lineEntries[1...].map({ Double($0) ?? 0.0 }))
            }
        }
    }
    
    return data
}

func parseSeriesLabels(fromDataSampleWithIndex index: Int) -> [String]? {
    let resourceName = String(format: "DataSample_%i", index)
    
    guard let dataPath = Bundle.main.path(forResource: resourceName, ofType: "csv") else {
        print(String(format: "Could Not Load Data Sample File %@", resourceName))
        return nil
    }
    
    var seriesLabels: [String] = []
    if let dataSampleString = try? String(contentsOfFile: dataPath) {
        for line in dataSampleString.components(separatedBy: "\n").dropFirst() {
            if let seriesLabel = line.components(separatedBy: ",").first {
                seriesLabels.append(seriesLabel)
            }
        }
    }
    
    return seriesLabels
}

func parseIndexLabels(fromDataSampleWithIndex index: Int) -> [String]? {
    let resourceName = String(format: "DataSample_%i", index)
    
    guard let dataPath = Bundle.main.path(forResource: resourceName, ofType: "csv") else {
        print(String(format: "Could Not Load Data Sample File %@", resourceName))
        return nil
    }
    
    var indexLabels: [String] = []
    if let dataSampleString = try? String(contentsOfFile: dataPath) {
        if let headerLine = dataSampleString.components(separatedBy: "\n").first {
            for indexLabel in headerLine.components(separatedBy: ",").dropFirst() {
                indexLabels.append(indexLabel)
            }
        }
    }
    
    return indexLabels
}
