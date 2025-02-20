import { Tabs } from "expo-router";
import { Image } from "react-native";

export default function AppLayout() {
  return (
    <Tabs>
      <Tabs.Screen
        name="home"
        options={{
          title: "",
          tabBarIcon: () => <Image source={{uri: "./../../assets/home-button.png"}}/>,
        }}
      />
    </Tabs>
  );
}