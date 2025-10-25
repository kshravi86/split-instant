import SwiftUI
import CoreData

struct GroupsListView: View {
    @Environment(\.managedObjectContext) private var viewContext
    
    // Placeholder FetchRequest - assumes Group entity exists in model
    @FetchRequest(
        sortDescriptors: [NSSortDescriptor(keyPath: \Group.createdDate, ascending: false)],
        animation: .default)
    private var groups: FetchedResults<Group>
    
    @State private var showingAddGroup = false

    var body: some View {
        List {
            ForEach(groups) { group in
                // Placeholder: NavigationLink to the group's expenses (NotesListView)
                NavigationLink(destination: NotesListView()) {
                    GroupRow(group: group)
                }
            }
            .onDelete(perform: deleteGroups)
        }
        .listStyle(.insetGrouped)
        .navigationTitle("Groups")
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button(action: { showingAddGroup = true }) {
                    Label("Add Group", systemImage: "person.3.fill")
                }
            }
            ToolbarItem(placement: .navigationBarLeading) {
                EditButton()
            }
        }
        .sheet(isPresented: $showingAddGroup) {
            GroupDetailView(group: nil)
        }
    }
    
    private func deleteGroups(offsets: IndexSet) {
        withAnimation {
            offsets.map { groups[$0] }.forEach(viewContext.delete)

            do {
                try viewContext.save()
            } catch {
                let nsError = error as NSError
                fatalError("Unresolved error \(nsError), \(nsError.userInfo)")
            }
        }
    }
}

struct GroupRow: View {
    // Note: This will crash if the Core Data model is not updated to include 'Group'
    @ObservedObject var group: Group
    
    var body: some View {
        HStack {
            Image(systemName: "person.3.fill")
                .foregroundColor(.blue)
                .font(.title2)
            
            VStack(alignment: .leading) {
                Text(group.name ?? "Untitled Group")
                    .font(.headline)
                
                // Placeholder for friend count
                Text("\(group.friends?.count ?? 0) members")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            // Placeholder for group balance
            Text("$0.00")
                .font(.subheadline)
                .foregroundColor(.green)
        }
        .padding(.vertical, 4)
    }
}

#Preview {
    GroupsListView()
        .environment(\.managedObjectContext, PersistenceController.preview.container.viewContext)
}