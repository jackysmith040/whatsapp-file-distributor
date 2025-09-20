## User Story
I want to send n number of fles (by default 300) maybe maximum 200 at a time.
The file is a pdf (report) in a folder.
We are sending the files to a whatsapp group. Certain files goto certain groups.

Draft Idea:
1. Select a folder (Take care of Operating system)
2. Selects Whatsapp group to send it to.
3. Sends in batches

## Select a folder
Let's make the desktop the default workspace.
We get only directories from the workspace as a menu and use numbers to select.
After selecting the folder it will ask if you are sure (with the folder name):
    if yes (you are sure) then we move to the next action. It also lists the files (it will ask you)
    if no we return to the menu, it will just suggest the next action.

## Whatsapp group logic
Gets only whatsapp groups.
A dictionary that maps the files to respective whatsapp group.
Create regex or pattern recognition for certain files to map them to certain folders.

SideNote: {
    Sort the files in terms of file size, smallest to biggest after grouping based on the pattern matching.
}

## Batch Logic
Find a way of sending them in batches.
Asynchronous? Yes we can do a bit of that. (Maybe Parallel?).Find which is simpler to implement.
Send to respective mapped groups.
Update user whenever an event is happening.

## Potential Failures
1. What if it breaks and doesn't send?
2. What if the network cuts or is slow and doesn't send reports?

Potential Solutions: {
    I'm thinking we could create a folder for files that weren't sent and at the end of the program we will alert the user that there is some unsent files.
}

SideNotes: {
    If there's success repsonse from that whatsapp wrapper we could update the sent_file tracker and compare it with the number of files tracker.
}

## For Now

We can use some OOP and dataclasses, i'll use functions though, mostly for utilities.
Classes
---
class Workspace:
    path: str
    exntension_allowed: list
    # add more later

class FolderReader

class WhatsappSender

class BatchSorter

class FileFailure

---

Errors: Files, Existence, Network.
Watchout: Take care of operating system path MacOS, Windows, Linux.

