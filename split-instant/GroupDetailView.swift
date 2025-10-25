import SwiftUI
import CoreData

struct GroupDetailView: View {
    @Environment(\.managedObjectContext) private var viewContext
    @Environment(\.dismiss) private var dismiss
    
    @State private var groupName: String
    @State private var newFriendName: String = ""
    
    let group: Group?
    
    init(group: Group?) {
        self.group = group
        _groupName = State(initialValue: group?.name ?? "")
    }
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Group Name")) {
                    TextField("e.g., Weekend Trip to Paris", text: $groupName)
                }
                
                Section(header: Text("Members")) {
                    // Placeholder for listing friends
                    Text("No members added yet.")
                        .foregroundColor(.secondary)
                    
                    HStack {
                        TextField("Add a friend's name", text: $newFriendName)
                        Button("Add") {
                            // Placeholder for adding friend logic
                            newFriendName = ""
                        }
                        .disabled(newFriendName.isEmpty)
                    }
                }
            }
            .navigationTitle(group == nil ? "New Group" : "Edit Group")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Save") {
                        saveGroup()
                        dismiss()
                    }
                    .disabled(groupName.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                }
            }
        }
    }
    
    private func saveGroup() {
        withAnimation {
            let groupToSave: Group
            
            if let existingGroup = group {
                groupToSave = existingGroup
            } else {
                groupToSave = Group(context: viewContext)
                groupToSave.createdDate = Date()
            }
            
            groupToSave.name = groupName.trimmingCharacters(in: .whitespacesAndNewlines)
            
            do {
                try viewContext.save()
            } catch {
                let nsError = error as NSError
                fatalError("Unresolved error \(nsError), \(nsError.userInfo)")
            }
        }
    }
}

#Preview {
    GroupDetailView(group: nil)
        .environment(\.managedObjectContext, PersistenceController.preview.container.viewContext)
}