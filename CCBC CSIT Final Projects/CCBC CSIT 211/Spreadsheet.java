package application;

import javafx.collections.ObservableList;
import javafx.collections.FXCollections;

public class Spreadsheet<T extends Person> {
	private ObservableList<T> faculty = FXCollections.observableArrayList();
	
	public void sort() {
		faculty = bubbleSort(faculty);
	}
	
	//Using a generic method + polymorphism lets us use the same function for both Teachers and Students
	private ObservableList<T> bubbleSort(ObservableList<T> array) {
		int pass = 0;
		int num_swaps = -1;
		while (num_swaps != 0) {
			num_swaps = 0;
			for (int i = 0; i < array.size() - pass - 1; i++) { //-1 since there will always be 1 less pair than the number of elements
				T a = array.get(i);
				T b = array.get(i + 1);
				if (a.getName().compareTo(b.getName()) > 0) {
					array.set(i, b);
					array.set(i + 1, a);
					num_swaps++;
				}
			}
			pass++;
		}
		return array;
	}
	
	public int search(String name) {
		int index = recursiveSearch(name, 0, faculty);
		return index;
	}
	
	private int recursiveSearch(String name, int index, ObservableList<T> personList) {
		Person currentPerson = personList.get(index);
		if (currentPerson.getName() == name) {
			return index;
		}
		else if (index == personList.size()) {
			return -1;
		}
		else {
			return recursiveSearch(name, ++index, personList);
		}
	}
	
	public void setFaculty(ObservableList<T> faculty) {
		this.faculty = faculty;
	}
	
	public ObservableList<T> getFaculty(){
		return faculty;
	}
	
	public void add(T person) {
		faculty.add(person);
	}
	
	public void addAtIndex(int index, T person) {
		faculty.add(index, person);
	}
}
