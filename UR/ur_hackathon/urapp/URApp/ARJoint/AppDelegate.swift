//
//  ViewController.swift
//  test
//
//  Created by XavierRoma on 08/03/2019.
//  Copyright © 2019 Salle URL. All rights reserved.
//

import UIKit
import ApiAI
import CoreData

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?


    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        // Override point for customization after application launch.
        let configuration = AIDefaultConfiguration()
        configuration.clientAccessToken = "9e63fce3110f491bbb8dcbe5787c76e9"
        
        let apiai = ApiAI.shared()
        apiai?.configuration = configuration
        
        UINavigationBar.appearance().barTintColor = UIColor.white
        UINavigationBar.appearance().backgroundColor = UIColor.white
        
        //* This Was Originally Set To False *//
        UINavigationBar.appearance().isTranslucent = true
        
        let statusBar: UIView = UIApplication.shared.value(forKey: "statusBar") as! UIView
        
        if statusBar.responds(to:#selector(setter: UIView.backgroundColor)) {
            statusBar.backgroundColor = UIColor.white
        }
        
        let fr = NSFetchRequest<Mov>(entityName: "Mov")
        let movements = try! self.persistentContainer.viewContext.fetch(fr)
        
        for movement in movements {
            self.persistentContainer.viewContext.delete(movement)
        }
        saveContext()
        
        /*if (movements.count == 0) {
            let m1 = NSEntityDescription.insertNewObject(forEntityName: "Mov", into: self.persistentContainer.viewContext) as! Mov
            m1.name = "bateria"
            m1.positions = "[-3.175, -3.01, 0.25, -1.52, 1.65, 1.6]"
            m1.order = 1
            m1.ventosa = false
            
            let m2 = NSEntityDescription.insertNewObject(forEntityName: "Mov", into: self.persistentContainer.viewContext) as! Mov
            m2.name = "bateria"
            m2.positions = "[-3.16, -2.62, 0.84, -2.52, 1.54, 1.6]"
            m2.order = 2
            m2.ventosa = false
            
            let m3 = NSEntityDescription.insertNewObject(forEntityName: "Mov", into: self.persistentContainer.viewContext) as! Mov
            m3.name = "bateria"
            m3.positions = "[-2.44, -2.89, 0.07, -1.4, 1.54, 1.6]"
            m3.order = 3
            m3.ventosa = false
            
            let m4 = NSEntityDescription.insertNewObject(forEntityName: "Mov", into: self.persistentContainer.viewContext) as! Mov
            m4.name = "bateria"
            m4.positions = "[-1.58, -1.06, -0.8, -1.54, 1.59, 0.775]"
            m4.order = 4
            m4.ventosa = false
            
            saveContext()
        }*/
        
        return true
    }

    func applicationWillResignActive(_ application: UIApplication) {
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and invalidate graphics rendering callbacks. Games should use this method to pause the game.
    }

    func applicationDidEnterBackground(_ application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    }

    func applicationWillEnterForeground(_ application: UIApplication) {
        // Called as part of the transition from the background to the active state; here you can undo many of the changes made on entering the background.
    }

    func applicationDidBecomeActive(_ application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
    }

    func applicationWillTerminate(_ application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
    }


    // MARK: - Core Data stack
    
    lazy var persistentContainer: NSPersistentContainer = {
        /*
         The persistent container for the application. This implementation
         creates and returns a container, having loaded the store for the
         application to it. This property is optional since there are legitimate
         error conditions that could cause the creation of the store to fail.
         */
        let container = NSPersistentContainer(name: "URApp")
        container.loadPersistentStores(completionHandler: { (storeDescription, error) in
            if let error = error as NSError? {
                // Replace this implementation with code to handle the error appropriately.
                // fatalError() causes the application to generate a crash log and terminate. You should not use this function in a shipping application, although it may be useful during development.
                
                /*
                 Typical reasons for an error here include:
                 * The parent directory does not exist, cannot be created, or disallows writing.
                 * The persistent store is not accessible, due to permissions or data protection when the device is locked.
                 * The device is out of space.
                 * The store could not be migrated to the current model version.
                 Check the error message to determine what the actual problem was.
                 */
                fatalError("Unresolved error \(error), \(error.userInfo)")
            }
        })
        return container
    }()
    
    // MARK: - Core Data Saving support
    
    func saveContext () {
        let context = persistentContainer.viewContext
        if context.hasChanges {
            do {
                try context.save()
            } catch {
                // Replace this implementation with code to handle the error appropriately.
                // fatalError() causes the application to generate a crash log and terminate. You should not use this function in a shipping application, although it may be useful during development.
                let nserror = error as NSError
                fatalError("Unresolved error \(nserror), \(nserror.userInfo)")
            }
        }
    }
    
}


