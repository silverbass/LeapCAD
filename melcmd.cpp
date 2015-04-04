#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <cassert>

using namespace std;

//enum cmdType {TRANSLATE, ROTATE, SCALE}

struct cmdType{
    int t;
    cmdType():t(0){}
    cmdType(int t1):t(t1){}
    // 1 is TRANSLATE
    // 2 is ROTATE
    // 3 is SCALE
    // 4 is CREATE SPHERE
};
struct pVec{
    int x,y,z;
    pVec(): x(0),y(0),z(0){}
    pVec(int x1, int y1, int z1): x(x1), y(y1), z(z1){}
};
int scalarMaker(int n){
    if(n==1){
        // TRANSLATE SCALAR
        return 1;
    }
    else if(n==2){
        //ROTATE SCALAR;
        return 1;
    }
    else if(n==3){
        //SCALE SCALAR;
        return 1;
    }
    else{
        cerr<<"ERROR: cmd not found: no "<<n<<endl;
        return 1;
    }
}
//returns a vector of strings that are MEL commands 
//to do a certain action
vector<string> melCmd(const cmdType & cmd, const pVec & v){
    //scalar for vector
    vector<string> melLines;
    string melLine ="";
    int k = scalarMaker(cmd.t);
    if(cmd.t==1){
        melLine.append("move -r ");
        melLine.append(to_string(k*v.x));
        melLine.append(" ");
        melLine.append(to_string(k*v.y));
        melLine.append(" ");
        melLine.append(to_string(k*v.z));
        melLine.append(";");
        melLines.push_back(melLine);
        melLine = "";
        return melLines;
    }
    else if(cmd.t==2){
        melLine.append("rotate -r ");
        melLine.append(to_string(k*v.x));
        melLine.append("deg ");
        melLine.append(to_string(k*v.y));
        melLine.append("deg ");
        melLine.append(to_string(k*v.z));
        melLine.append("deg;");
        melLines.push_back(melLine);
        melLine = "";
        return melLines;
    }
    else if(cmd.t==3){
        melLine.append("scale -r ");
        melLine.append(to_string(k*v.x));
        melLine.append(" ");
        melLine.append(to_string(k*v.y));
        melLine.append(" ");
        melLine.append(to_string(k*v.z));
        melLine.append(";");
        melLines.push_back(melLine);
        melLine = "";
        return melLines;
    }
    cerr<<"cmd not caught: "<<cmd.t<<endl;
    return melLines;
}

/*void write(vector<string> melLines)
{
    ofstream m_file;
    if (!melLines.empty())
    {
        m_file.open(mel_script.mel);
        m_file << melLines.front();
        melLines.erase(melLines.begin());
        m_file.close();
    }
    else
    {
        m_file.open(mel_script.mel);
        m_file << "";
        m_file.close();
    }
}*/

int main()
{
	ofstream m_file;
	m_file.open("mel_script.mel");
	vector<string> n;
    n.push_back("move -r 1 1 1;");
<<<<<<< Updated upstream
	for(vector<string>::iterator it = n.begin(); it !=n.end(); ++n){
		m_file<<*it<<endl;
	}
	m_file.close();
=======
    m_file << n[0];
    m_file.close();
>>>>>>> Stashed changes
    return 0;
}


