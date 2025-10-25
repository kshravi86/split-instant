import CoreData

// MARK: - Core Data Stubs (Assumes model update in NotesModel.xcdatamodel)

@objc(Group)
public class Group: NSManagedObject {
    @NSManaged public var name: String?
    @NSManaged public var createdDate: Date?
    @NSManaged public var friends: NSSet? // Relationship to Friend
}

@objc(Friend)
public class Friend: NSManagedObject {
    @NSManaged public var name: String?
    @NSManaged public var group: Group? // Relationship to Group
}

extension Group: Identifiable {}
extension Friend: Identifiable {}
