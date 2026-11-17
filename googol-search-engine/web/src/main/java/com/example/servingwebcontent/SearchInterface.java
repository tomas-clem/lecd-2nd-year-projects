package com.example.servingwebcontent;

import java.io.IOException;
import java.rmi.NotBoundException;
import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.ArrayList;
import java.util.HashSet;

public interface SearchInterface extends Remote{
    public ArrayList<Result> search(String query, int page) throws IOException, NotBoundException;
    public HashSet<String> searchConnections(String url) throws RemoteException;
    public void addFirstInQueue(String url) throws RemoteException;
}
