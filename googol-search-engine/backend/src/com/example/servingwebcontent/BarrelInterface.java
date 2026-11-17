package com.example.servingwebcontent;

import java.rmi.Remote;
import java.util.HashSet;

public interface BarrelInterface extends Remote {
    public void addToIndex(String word, String url) throws java.rmi.RemoteException;
    public HashSet<String> searchSingleWord(String word) throws java.rmi.RemoteException;
    public HashSet<String> getConnections(String url) throws java.rmi.RemoteException;
    public void addConnections(String urlPage, String urlMencioned) throws java.rmi.RemoteException;
    public String getUrl() throws java.rmi.RemoteException;
    public void addToQueue(String url) throws java.rmi.RemoteException;
    public void addFirstInQueue(String url) throws java.rmi.RemoteException;
    public  int QueueNumber() throws java.rmi.RemoteException;
}
