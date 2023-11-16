import { useRouter } from "expo-router";
import { StyleSheet, Text, View, Button } from "react-native";

const WelcomeScreen = () => {
  const navigation = useRouter();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Sports Betting</Text>
      <Text style={styles.subtitle}>Demo App</Text>
      <Button title="Continue" onPress={() => navigation.push("/home")} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "dark-green",
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    textAlign: "center",
  },
});

export default WelcomeScreen;